/**
 * dashboard.js — TaskFlow
 * Maneja: panel de detalle, eliminar, quick-add, completar, colores de paleta
 */

/* ═══════════════════════════════════════════
   PANEL DE DETALLE
════════════════════════════════════════════ */

/**
 * Abre el panel lateral con los datos de la tarea clickeada.
 * Lee los data-* attributes del card.
 */
function openDetail(el) {
    const id           = el.getAttribute('data-id');
    const titulo       = el.getAttribute('data-titulo');
    const desc         = el.getAttribute('data-desc');
    const prioridad    = el.getAttribute('data-prioridad');   // 'A', 'M', 'B'
    const fecha        = el.getAttribute('data-fecha');       // 'YYYY-MM-DD'
    const categoriaId  = el.getAttribute('data-categoria-id');
    const updated      = el.getAttribute('data-updated');

    // Rellenar campos
    document.getElementById('detTitle').value = titulo;
    document.getElementById('detDesc').value  = desc;
    document.getElementById('detFecha').value = fecha || '';

    // Prioridad + estilo visual del select
    const selPrio = document.getElementById('detPrioridad');
    selPrio.value = prioridad || 'M';
    updatePrioStyle(selPrio);

    // Categoría
    const selCat = document.getElementById('detCategoria');
    selCat.value = categoriaId || '';

    // Última actualización
    const updEl = document.getElementById('detUpdated');
    updEl.textContent = updated ? `Last updated: ${updated}` : '';

    // Acción del form de edición
    document.getElementById('editForm').action = `/editar/${id}/`;

    // Acción del form de delete (desde panel)
    document.getElementById('deleteFormPanel').action = `/eliminar/${id}/`;

    // Abrir panel y overlay
    document.getElementById('detailPanel').classList.remove('hidden');
    document.getElementById('panelOverlay').classList.remove('hidden');

    // Marca visual en la card
    document.querySelectorAll('.task-card').forEach(c => c.classList.remove('selected'));
    el.classList.add('selected');
}

/** Cierra el panel lateral */
function closeDetail() {
    document.getElementById('detailPanel').classList.add('hidden');
    document.getElementById('panelOverlay').classList.add('hidden');
    document.querySelectorAll('.task-card').forEach(c => c.classList.remove('selected'));
}

/**
 * Cambia el color/estilo del select de prioridad según el valor elegido.
 * Llama con el elemento <select> como parámetro.
 */
function updatePrioStyle(select) {
    select.classList.remove('prio-a', 'prio-m', 'prio-b');
    const map = { A: 'prio-a', M: 'prio-m', B: 'prio-b' };
    if (map[select.value]) select.classList.add(map[select.value]);
}

/* ═══════════════════════════════════════════
   ELIMINAR TAREA — desde card o desde panel
════════════════════════════════════════════ */

/**
 * Dispara el modal de confirmación desde un click en la card directamente.
 * @param {HTMLElement} card — el .task-card
 */
function submitDelete(card) {
    const id    = card.getAttribute('data-id');
    const title = card.getAttribute('data-titulo');

    document.getElementById('deleteTaskName').innerText = title;
    document.getElementById('customConfirmModal').classList.remove('hidden');

    // El form principal de delete
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.action = `/eliminar/${id}/`;

    document.getElementById('confirmDeleteBtn').onclick = function () {
        deleteForm.submit();
    };
}

/**
 * Dispara el modal de confirmación desde el botón dentro del panel.
 * Usa el form de delete del panel (deleteFormPanel) que ya tiene la action seteada.
 */
function submitDeleteFromPanel() {
    const title  = document.getElementById('detTitle').value;
    const action = document.getElementById('deleteFormPanel').action;

    document.getElementById('deleteTaskName').innerText = title;
    document.getElementById('customConfirmModal').classList.remove('hidden');

    // Reutilizamos el deleteForm apuntando a la misma action
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.action = action;

    document.getElementById('confirmDeleteBtn').onclick = function () {
        deleteForm.submit();
    };
}

/** Cierra el modal de confirmación */
function closeCustomConfirm() {
    document.getElementById('customConfirmModal').classList.add('hidden');
}

/* ═══════════════════════════════════════════
   MARCAR COMO COMPLETADA
════════════════════════════════════════════ */

/**
 * Toggle visual inmediato y envía POST al backend.
 * El backend debe tener una ruta /completar/<id>/ que hace flip del campo.
 */
function toggleComplete(event, id, btn) {
    event.stopPropagation(); // No abrir el panel

    const card = btn.closest('.task-card');
    const isCompleted = btn.classList.contains('checked');

    // Efecto visual inmediato
    btn.classList.toggle('checked');
    card.classList.toggle('task-completed');

    // Actualizar ícono
    btn.innerHTML = btn.classList.contains('checked')
        ? '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
        : '';

    // Enviar al servidor (fetch silencioso)
    fetch(`/completar/${id}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(res => {
        if (!res.ok) throw new Error('Error al completar');
        showToast(btn.classList.contains('checked') ? '✓ Tarea completada' : 'Tarea reabierta', 'success');
    })
    .catch(() => {
        // Revertir si falla
        btn.classList.toggle('checked');
        card.classList.toggle('task-completed');
        showToast('Error al actualizar la tarea', 'error');
    });
}

/* ═══════════════════════════════════════════
   QUICK ADD
════════════════════════════════════════════ */

/** Muestra el input de nueva tarea */
function showQuickAdd() {
    document.getElementById('quickAddTrigger').classList.add('hidden');
    document.getElementById('quickAddForm').classList.remove('hidden');
    document.getElementById('quickAddInput').focus();
}

/** Oculta el quick add y vuelve al trigger */
function hideQuickAdd() {
    document.getElementById('quickAddForm').classList.add('hidden');
    document.getElementById('quickAddTrigger').classList.remove('hidden');
    document.getElementById('quickAddInput').value = '';
}

// Enter = submit, Esc = cancelar
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('quickAddInput');
    if (!input) return;

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            if (input.value.trim()) {
                input.closest('form').submit();
            }
        }
        if (e.key === 'Escape') {
            hideQuickAdd();
        }
    });
});

/* ═══════════════════════════════════════════
   MODAL CATEGORÍA — paleta de colores
════════════════════════════════════════════ */

function openCatModal() {
    document.getElementById('modalCat').classList.remove('hidden');
}

function closeCatModal() {
    document.getElementById('modalCat').classList.add('hidden');
}

/**
 * Selecciona un color de la paleta.
 * @param {HTMLElement} btn — el botón .color-swatch clickeado
 */
function selectColor(btn) {
    document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('selectedColor').value = btn.getAttribute('data-color');
}

/* ═══════════════════════════════════════════
   TOAST
════════════════════════════════════════════ */

let toastTimeout;

/**
 * Muestra un toast de notificación.
 * @param {string} msg — mensaje
 * @param {'success'|'error'} type
 */
function showToast(msg, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.className = `toast ${type}`;
    // Forzar reflow para reiniciar animación
    void toast.offsetWidth;
    toast.classList.add('show');

    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.classList.add('hidden'), 300);
    }, 2800);
}

/* ═══════════════════════════════════════════
   UTILS
════════════════════════════════════════════ */

/** Obtiene el valor de una cookie por nombre (para CSRF) */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const c = cookie.trim();
            if (c.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(c.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Cerrar modales con Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeDetail();
        closeCatModal();
        closeCustomConfirm();
    }
});