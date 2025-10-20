/** 
 * @typedef {Object} Task
 * @property {string} id - ID da task que especifica ela dentro do banco de dados 
 * @property {string} task - Conteúdo principal da task para identificar ela
 * @property {boolean} task_conclusion - Status de conclusão da task
 * @property {string} task_description - Descrição detalhada da task
 * @property {string} user_id - ID do usuário responsável pela task
 */
import TaskService from "./taskService";

const allTasksList = document.getElementById("todo-all-list");
const activeTasksList = document.getElementById("todo-active-list");
const doneTasksList = document.getElementById("todo-done-list");

// Cache das tasks para atualização em tempo real
let currentTasks = [];

class TaskUIManager {
    static initializeEventListeners() {
        this.addInteractivityCustomization(allTasksList);
        this.addInteractivityCustomization(activeTasksList);
        this.addInteractivityCustomization(doneTasksList);
    }

    static addInteractivityCustomization(listElement) {
        listElement.addEventListener("click", async (event) => {
            if (event.target.classList.contains("form-check-input")) {
                const checkbox = event.target;
                const taskId = checkbox.id;
                const content = checkbox.nextElementSibling;
                const isChecked = checkbox.checked;

                // Atualizar visualmente
                this.updateCheckboxVisual(checkbox, content, isChecked);

                // Encontrar a task no cache
                const taskIndex = currentTasks.findIndex(task => task.id === taskId);
                if (taskIndex !== -1) {
                    // Atualizar no cache
                    currentTasks[taskIndex].task_conclusion = isChecked;
                    
                    try {
                        // Atualizar no banco de dados
                        await TaskService.updateTaskStatus(taskId, isChecked);
                        
                        // Atualizar todas as listas
                        this.updateAllTaskLists();
                    } catch (error) {
                        // Reverter a mudança visual em caso de erro
                        console.error("Falha ao atualizar task:", error);
                        checkbox.checked = !isChecked;
                        this.updateCheckboxVisual(checkbox, content, !isChecked);
                    }
                }
            }
        });
    }

    static updateCheckboxVisual(checkbox, content, isChecked) {
        if (!isChecked) {
            content.classList.remove("text-decoration-line-through", "text-secondary");
        } else {
            content.classList.add("text-decoration-line-through", "text-secondary");
        }
    }

    static createListItem(task) {
        const checkedAttr = task.task_conclusion ? "checked" : "";
        const textDecorationClass = task.task_conclusion ? "text-decoration-line-through text-secondary" : "";
        
        const taskStructureString = 
            `
            <li class="list-group-item">
                <input type="checkbox" class="form-check-input me-1" id="${task.id}" ${checkedAttr}>
                <label class="form-check-label ${textDecorationClass}" for="${task.id}">
                    <strong>${this.escapeHtml(task.task)}:</strong> ${this.escapeHtml(task.task_description)}
                </label> 
            </li>
            `;
        return taskStructureString;
    }

    static escapeHtml(str) {
        if (str === null || str === undefined) return "";
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");
    }

    static updateAllTaskLists() {
        if (!Array.isArray(currentTasks)) return;
        
        // Lista "Todas" - mostra tudo
        allTasksList.innerHTML = '';
        currentTasks.forEach(task => {
            const listItem = this.createListItem(task);
            allTasksList.insertAdjacentHTML("beforeend", listItem);
        });
        
        // Lista "Ativas" - mostra apenas não concluídas
        activeTasksList.innerHTML = '';
        const activeTasks = currentTasks.filter(task => !task.task_conclusion);
        activeTasks.forEach(task => {
            const listItem = this.createListItem(task);
            activeTasksList.insertAdjacentHTML("beforeend", listItem);
        });
        
        // Lista "Concluídas" - mostra apenas concluídas
        doneTasksList.innerHTML = '';
        const doneTasks = currentTasks.filter(task => task.task_conclusion);
        doneTasks.forEach(task => {
            const listItem = this.createListItem(task);
            doneTasksList.insertAdjacentHTML("beforeend", listItem);
        });
        
        // Re-aplicar os event listeners após atualizar o DOM
        this.initializeEventListeners();
    }

    /**
     * @param {Task[]} tasks - Array de tasks para listar
     */
    static listItems(tasks) {
        if (!Array.isArray(tasks)) return;
        
        // Guardar tasks no cache
        currentTasks = tasks;
        
        // Atualizar todas as listas
        this.updateAllTaskLists();
    }

    static async reloadTasks() {
        try {
            const tasks = await TaskService.getAllTasks();
            this.listItems(tasks);
            return tasks;
        } catch (error) {
            console.error("Erro ao recarregar tasks:", error);
            return [];
        }
    }

    // Método para adicionar nova task ao cache e atualizar UI
    static addNewTask(task) {
        if (!currentTasks.find(t => t.id === task.id)) {
            currentTasks.push(task);
            this.updateAllTaskLists();
        }
    }

    // Método para remover task do cache e atualizar UI
    static removeTask(taskId) {
        currentTasks = currentTasks.filter(task => task.id !== taskId);
        this.updateAllTaskLists();
    }

    // Getter para acessar tasks atuais
    static getCurrentTasks() {
        return [...currentTasks]; // Retorna cópia para evitar mutação externa
    }
}

// Inicialização quando o DOM estiver carregado
document.addEventListener("DOMContentLoaded", () => {
    console.log("Carregando javascript...");
    
    // Inicializar event listeners
    TaskUIManager.initializeEventListeners();
    
    // Carregar tasks iniciais
    if (typeof tasksJson === 'string') {
        TaskUIManager.listItems(JSON.parse(tasksJson));
    } else if (tasksJson) {
        TaskUIManager.listItems(tasksJson);
    } else {
        // Se não houver tasksJson, carregar do servidor
        TaskUIManager.reloadTasks();
    }

    console.log("Javascript carregado");
});