function openDetail(el) {
    const id = el.getAttribute('data-id');
    const titulo = el.getAttribute('data-titulo');
    const desc = el.getAttribute('data-desc');

    const panel = document.getElementById('detailPanel');
    panel.classList.remove('hidden');

    document.getElementById('detTitle').value = titulo;
    document.getElementById('detDesc').value = desc;

    // ✅ Rutas corregidas — coinciden con tareas/urls.py bajo el prefijo ''
    document.getElementById('editForm').action = '/editar/' + id + '/';
    document.getElementById('deleteForm').action = '/eliminar/' + id + '/';

    // Efecto de selección visual
    document.querySelectorAll('.task-card').forEach(c => c.style.borderColor = 'transparent');
    el.style.borderColor = '#10b981';
}

function closeDetail() {
    document.getElementById('detailPanel').classList.add('hidden');
    document.querySelectorAll('.task-card').forEach(c => c.style.borderColor = 'transparent');
}

function submitDelete() {
    const title = document.getElementById('detTitle').value;
    document.getElementById('deleteTaskName').innerText = title;
    document.getElementById('customConfirmModal').classList.remove('hidden');

    document.getElementById('confirmDeleteBtn').onclick = function () {
        document.getElementById('deleteForm').submit();
    };
}

function openCatModal() { document.getElementById('modalCat').classList.remove('hidden'); }
function closeCatModal() { document.getElementById('modalCat').classList.add('hidden'); }
function closeCustomConfirm() { document.getElementById('customConfirmModal').classList.add('hidden'); }