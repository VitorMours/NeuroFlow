export default class TaskService {
    static api = "http://localhost:5000";
    static config = {
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include"
    };

    /**
     * Atualiza o status de uma task no banco de dados
     * @param {string} taskId - ID da task
     * @param {boolean} newStatus - Novo status de conclusão
     */
    static async updateTaskStatus(taskId, newStatus) {
        
        try {
            const response = await fetch(`${this.api}/todo`, {
                method: "PUT",
                headers: this.config.headers,
                credentials: this.config.credentials,
                body: JSON.stringify({
                    task_conclusion: newStatus,
                    task_id: taskId
                })
            });
            
            if (!response.ok) {
                throw new Error(`Erro na requisição: ${response.status}`);
            }
            
            const result = await response.json();
            return result;
            
        } catch (error) {
            throw error; // Propaga o erro para o caller
        }
    }

    /**
     * Busca todas as tasks do usuário
     */
    static async getAllTasks() {
        try {
            const response = await fetch(`${this.api}/todo`, {
                method: "GET",
                credentials: this.config.credentials
            });
            
            if (!response.ok) {
                throw new Error(`Erro na requisição: ${response.status}`);
            }
            
            const tasks = await response.json();
            return tasks;
            
        } catch (error) {
            console.error("Erro ao buscar tasks:", error);
            return [];
        }
    }

    /**
     * Busca tasks de um usuário específico
     * @param {string} userId - ID do usuário
     */
    static async getUserTasks(userId) {
        try {
            const response = await fetch(`${this.api}/todo/user/${userId}`, {
                method: "GET",
                credentials: this.config.credentials
            });
            
            if (!response.ok) {
                throw new Error(`Erro na requisição: ${response.status}`);
            }
            
            const tasks = await response.json();
            return tasks;
            
        } catch (error) {
            console.error("Erro ao buscar tasks do usuário:", error);
            return [];
        }
    }
}