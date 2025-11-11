from ..models import db
from typing import List, Optional
from src.models.task_model import Task
from src.models.user_model import User

class TaskRepository:
    
    @staticmethod 
    def create(task_data: dict, user_id: User) -> None:
        """
        Create a new task in the database based on the user as the foreign key.
        """
        needed_fields = ["task","task_description","task_conclusion"]
        
        for field in needed_fields:
            if field not in task_data.keys():
                return False

        new_task = Task(
                task = task_data["task"],
                task_description = task_data["task_description"],
                task_conclusion = task_data["task_conclusion"],
                user_id = user_id
                )
        db.session.add(new_task)
        db.session.commit()
        return new_task
    
    @staticmethod   
    def update(task_id: int, update_data: dict, user_id: Optional[int] = None) -> Optional[Task]:
        """
        Atualiza uma task com base nos dados do usuario e no novo conteudo.
        
        Args:
            task_id: ID da task a ser atualizada
            update_data: Dicionário com os campos a serem atualizados
            user_id: ID do usuário (opcional para verificação de propriedade)
        
        Returns:
            Task: A task modificada se a atualização for bem sucedida, None caso contrário
        """
        try:
            # Buscar a task pelo ID
            task = Task.query.get(task_id)
            
            if not task:
                print(f"Task with ID {task_id} not found")
                return None
            
            # Verificar se o usuário é o dono da task (se user_id for fornecido)
            if user_id and task.user_id != user_id:
                print(f"User {user_id} is not the owner of task {task_id}")
                return None
            
            # Campos permitidos para atualização
            allowed_fields = [
                "task", 
                "task_description", 
                "task_conclusion", 
                "task_priority",
                "task_due_date"
            ]
            
            # Atualizar apenas campos permitidos que existem no modelo
            updated = False
            for field, value in update_data.items():
                if field in allowed_fields and hasattr(task, field):
                    setattr(task, field, value)
                    updated = True
            
            # Se nenhum campo foi atualizado, retornar None
            if not updated:
                print("No valid fields to update")
                return None
            
            # Commit das alterações
            db.session.commit()
            
            print(f"Task {task_id} updated successfully")
            return task
            
        except Exception as e:
            db.session.rollback()
            print(f"Error updating task {task_id}: {str(e)}")
            return None

    @staticmethod
    def delete(id: int) -> bool:
        """
        Deve deletar uma task com base no seu id, retornando true se for deletado
        """
        if task := Task.query.filter_by(id=id).first():
            try:
                db.session.delete(task)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Error deleting task {id}: {str(e)}")
            
        return False
    
    @staticmethod
    def get_all() -> List[Task]:
        """
        Pega todas as tasks presentes dentro do banco de dados
        """
        if Task.query.count() == 0:
            return []
        return Task.query.all()  
    
    @staticmethod
    def get_by_email(email: str) -> List[Task]:
        """
        Retorna todas as tasks baseadas no email do usuario dono
        dessa determinada task
        """
        if Task.query.count() == 0:
            return []
        return Task.query.join(User).filter(User.email == email).all()        

    @staticmethod
    def get_by_uuid(uuid: str) -> Optional[Task]:
        """
        Busca uma task pelo UUID
        """
        if not uuid:
            return None 
        
        return Task.query.filter_by(id=uuid).first()

    @staticmethod
    def get_by_id_and_user(task_id: int, user_id: int) -> Optional[Task]:
        """
        Busca uma task pelo ID e verifica se pertence ao usuário
        """
        return Task.query.filter_by(id=task_id, user_id=user_id).first()

    def __repr__(self) -> str:
        return "<TaskRepository>"

    def __str__(self) -> str:
        return "<TaskRepository>"