from typing import Tuple, Union
from flask import Blueprint, redirect, render_template, flash, request, session, url_for, jsonify
from flask.views import MethodView, View
from ..services.task_service import TaskService
from src.utils.security import login_required, sanitize_request
from src.forms import TaskForm 
import json

bp = Blueprint("home", __name__)

class HomeView(View):
    decorators = [login_required]

    def dispatch_request(self) -> str:
        return render_template("home.html", active_page="home")

class NotesView(MethodView):
    decorators = [login_required]

    def get(self) -> str:
        return render_template("notes.html", active_page="notes")

class NoteTakerView(MethodView):
    decorators = [login_required]

    def get(self, note_uuid: int) -> str:
        # TODO: Fazer esse método para retornar um template da nota, especificado com base na rota
        # note = Note
        # return render_template("note_taker.html", note_uuid = note_uuid active_page="notes")
        pass

class TodoView(MethodView):
    decorators = [login_required]

    def get(self) -> str:
        form = TaskForm()
        
        tasks = TaskService.get_user_tasks(session.get("email"))
        tasks_serialized = [t.to_json() for t in tasks]
        return render_template("todo.html", active_page="todo", tasks = tasks_serialized, form = form)
    
    def post(self) -> str:
        form = TaskForm()
        if form.validate_on_submit():
            try:
                data = form.data 
                data["task_conclusion"] = False
                TaskService.create(data)
                print(f"dados tratados: {data}")
                flash("Task created successfully!", "success")    
            except Exception as e:
                flash("An error occurred while creating the task.", "danger")
        else:
            flash("Invalid form data. Please check your input.", "warning")
        return redirect(url_for("views.home.todo"))

    def put(self) -> Union[bool, Tuple[str, int]]:
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            if "task_id" not in data:
                return jsonify({"error": "Task ID is required"}), 400
            
            task_id = data.get("task_id")
            update_data = {k: v for k, v in data.items() if k != "task_id"}
            
            success = TaskService.update(task_id, update_data)
            
            # CORREÇÃO: Retornar uma resposta válida em vez de None
            if success:
                return jsonify({"message": "Task updated successfully"}), 200
            else:
                return jsonify({"error": "Task not found or update failed"}), 404
                
        except Exception as e:
            print(f"Error in PUT method: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500


bp.add_url_rule("/home", view_func=HomeView.as_view("home"))
bp.add_url_rule("/notes", view_func=NotesView.as_view("notes"))
bp.add_url_rule("/todo", view_func=TodoView.as_view("todo"))
