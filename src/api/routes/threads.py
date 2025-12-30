"""Thread management API endpoints."""

import json
from flask import Blueprint, request, jsonify, Response

from src.logger import get_logger
from src.db.threads import (
    create_thread,
    get_thread,
    list_threads,
    update_thread_title,
    delete_thread,
    add_message,
    get_messages
)
from src.db.checkpointer import PostgresCheckpointer
from src.agents.graph import create_clinical_graph

logger = get_logger(__name__)

threads_bp = Blueprint('threads', __name__)

_graph = None
_checkpointer = None


def get_graph_with_checkpointer():
    """Get graph with PostgreSQL checkpointer."""
    global _graph, _checkpointer
    
    if _checkpointer is None:
        _checkpointer = PostgresCheckpointer()
    
    if _graph is None:
        logger.info("Initializing clinical graph with checkpointer...")
        _graph = create_clinical_graph(checkpointer=_checkpointer)
        logger.info("Clinical graph with checkpointer initialized")
    
    return _graph


@threads_bp.route('/threads', methods=['GET'])
def list_all_threads():
    """List all chat threads."""
    logger.info("Listing all threads")
    try:
        threads = list_threads()
        return jsonify(threads)
    except Exception as e:
        logger.exception(f"Failed to list threads: {e}")
        return jsonify({"error": str(e)}), 500


@threads_bp.route('/threads', methods=['POST'])
def create_new_thread():
    """Create a new chat thread."""
    data = request.get_json() or {}
    title = data.get("title", "New Chat")
    
    logger.info(f"Creating new thread: {title}")
    try:
        thread = create_thread(title)
        return jsonify(thread), 201
    except Exception as e:
        logger.exception(f"Failed to create thread: {e}")
        return jsonify({"error": str(e)}), 500


@threads_bp.route('/threads/<thread_id>', methods=['GET'])
def get_thread_detail(thread_id: str):
    """Get thread with messages."""
    logger.info(f"Getting thread {thread_id}")
    try:
        thread = get_thread(thread_id)
        if not thread:
            return jsonify({"error": "Thread not found"}), 404
        
        messages = get_messages(thread_id)
        thread["messages"] = messages
        return jsonify(thread)
    except Exception as e:
        logger.exception(f"Failed to get thread: {e}")
        return jsonify({"error": str(e)}), 500


@threads_bp.route('/threads/<thread_id>', methods=['PATCH'])
def update_thread(thread_id: str):
    """Update thread title."""
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing 'title' field"}), 400
    
    logger.info(f"Updating thread {thread_id}")
    try:
        thread = update_thread_title(thread_id, data["title"])
        if not thread:
            return jsonify({"error": "Thread not found"}), 404
        return jsonify(thread)
    except Exception as e:
        logger.exception(f"Failed to update thread: {e}")
        return jsonify({"error": str(e)}), 500


@threads_bp.route('/threads/<thread_id>', methods=['DELETE'])
def delete_thread_endpoint(thread_id: str):
    """Delete a thread."""
    logger.info(f"Deleting thread {thread_id}")
    try:
        deleted = delete_thread(thread_id)
        if not deleted:
            return jsonify({"error": "Thread not found"}), 404
        return jsonify({"success": True})
    except Exception as e:
        logger.exception(f"Failed to delete thread: {e}")
        return jsonify({"error": str(e)}), 500


@threads_bp.route('/threads/<thread_id>/query', methods=['POST'])
def query_thread(thread_id: str):
    """Query with thread context."""
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' field"}), 400
    
    query_text = data["query"]
    logger.info(f"Query in thread {thread_id}: '{query_text[:50]}...'")
    
    try:
        thread = get_thread(thread_id)
        if not thread:
            return jsonify({"error": "Thread not found"}), 404
        
        add_message(thread_id, "user", query_text)
        
        graph = get_graph_with_checkpointer()
        config = {"configurable": {"thread_id": thread_id}}
        
        result = graph.invoke({
            "query": query_text,
            "route": None,
            "tools_results": [],
            "orgs_results": [],
            "response": "",
            "error": None
        }, config)
        
        route = result.get("route")
        response = result.get("response", "")
        
        add_message(thread_id, "assistant", response, route)
        
        if thread["title"] == "New Chat" and response:
            new_title = query_text[:50] + ("..." if len(query_text) > 50 else "")
            update_thread_title(thread_id, new_title)
        
        logger.info(f"Query processed: route={route}")
        
        return jsonify({
            "route": route,
            "response": response,
            "tools_results": result.get("tools_results", []),
            "orgs_results": result.get("orgs_results", [])
        })
    except Exception as e:
        logger.exception(f"Failed to process query: {e}")
        return jsonify({"error": str(e)}), 500


@threads_bp.route('/threads/<thread_id>/query/stream', methods=['POST'])
def query_thread_stream(thread_id: str):
    """Streaming query with thread context."""
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' field"}), 400
    
    query_text = data["query"]
    logger.info(f"Stream query in thread {thread_id}: '{query_text[:50]}...'")
    
    def generate():
        try:
            thread = get_thread(thread_id)
            if not thread:
                yield f"data: {json.dumps({'error': 'Thread not found'})}\n\n"
                return
            
            add_message(thread_id, "user", query_text)
            
            graph = get_graph_with_checkpointer()
            config = {"configurable": {"thread_id": thread_id}}
            
            initial_state = {
                "query": query_text,
                "route": None,
                "tools_results": [],
                "orgs_results": [],
                "response": "",
                "error": None
            }
            
            final_response = ""
            final_route = ""
            
            for event in graph.stream(initial_state, config):
                node_name = list(event.keys())[0]
                node_output = event[node_name]
                
                logger.info(f"Stream event: {node_name}")
                
                if node_output.get("route"):
                    final_route = node_output["route"]
                if node_output.get("response"):
                    final_response = node_output["response"]
                
                sse_data = {"node": node_name, "data": node_output}
                yield f"data: {json.dumps(sse_data)}\n\n"
            
            if final_response:
                add_message(thread_id, "assistant", final_response, final_route)
            
            if thread["title"] == "New Chat" and query_text:
                new_title = query_text[:50] + ("..." if len(query_text) > 50 else "")
                update_thread_title(thread_id, new_title)
            
            logger.info("Stream completed")
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            logger.exception(f"Stream error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )
