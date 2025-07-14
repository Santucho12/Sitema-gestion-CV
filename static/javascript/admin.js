 // --- JS modularizado y simplificado ---
        function eliminarPostulante(btn, id) {
            if (!confirm('¿Seguro que quieres eliminar este postulante?')) return;
            fetch('/admin/eliminar_postulante', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) btn.closest('tr').remove();
                else alert('Error al eliminar postulante');
            })
            .catch(() => alert('Error de conexión'));
        }

        function filtrarTabla() {
            const nombre = document.getElementById('filtroNombre').value.trim().toLowerCase();
            const apellido = document.getElementById('filtroApellido').value.trim().toLowerCase();
            document.querySelectorAll('table tbody tr').forEach(row => {
                const nombreCelda = row.children[2].textContent.trim().toLowerCase();
                const apellidoCelda = row.children[3].textContent.trim().toLowerCase();
                row.style.display = ( (!nombre || nombreCelda.includes(nombre)) && (!apellido || apellidoCelda.includes(apellido)) ) ? '' : 'none';
            });
        }
        document.getElementById('filtroNombre').addEventListener('input', filtrarTabla);
        document.getElementById('filtroApellido').addEventListener('input', filtrarTabla);

        document.getElementById('darkModeBtn').addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            this.textContent = document.body.classList.contains('dark-mode') ? '☀️ Modo claro' : '🌙 Modo oscuro';
        });

        function crearEstrellas(cell, value) {
            cell.innerHTML = '';
            for (let i = 1; i <= 5; i++) {
                const star = document.createElement('span');
                star.textContent = '★';
                star.dataset.value = i;
                star.style.cursor = 'pointer';
                star.style.color = i <= value ? '#ffc107' : '#999';
                star.addEventListener('mouseover', () => resaltar(cell, i));
                star.addEventListener('mouseout', () => resaltar(cell, value));
                star.addEventListener('click', () => calificar(cell, i));
                cell.appendChild(star);
            }
        }
        function resaltar(cell, val) {
            cell.querySelectorAll('span').forEach((star, idx) => {
                star.style.color = idx < val ? '#ffc107' : '#999';
            });
        }
        function calificar(cell, value) {
            cell.dataset.value = value;
            resaltar(cell, value);
            fetch('/admin/calificar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id_postulante: cell.dataset.id, calificacion: value })
            })
            .then(r => r.json())
            .then(data => { cell.title = data.success ? 'Calificación guardada' : 'Error al guardar'; })
            .catch(() => { cell.title = 'Error de conexión'; });
        }
        document.querySelectorAll('.rating').forEach(cell => {
            crearEstrellas(cell, parseInt(cell.dataset.value) || 0);
        });

        // Ordenar por ID descendente al cargar
        document.addEventListener('DOMContentLoaded', function() {
            const tbody = document.querySelector('table tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            rows.sort((a, b) => (parseInt(b.children[0].textContent) || 0) - (parseInt(a.children[0].textContent) || 0));
            rows.forEach(row => tbody.appendChild(row));
            let sortState = {};
            document.querySelectorAll('th.sortable').forEach(th => {
                th.addEventListener('click', function() {
                    const colIndex = parseInt(th.getAttribute('data-col'));
                    const rows = Array.from(tbody.querySelectorAll('tr'));
                    sortState[colIndex] = !sortState[colIndex];
                    const isDesc = sortState[colIndex];
                    let sortFn;
                    if (colIndex === 21) {
                        sortFn = (a, b) => {
                            const aVal = parseInt(a.querySelector('.rating').dataset.value) || 0;
                            const bVal = parseInt(b.querySelector('.rating').dataset.value) || 0;
                            return isDesc ? bVal - aVal : aVal - bVal;
                        };
                    } else {
                        sortFn = (a, b) => {
                            const aVal = a.children[colIndex].textContent.trim().toLowerCase();
                            const bVal = b.children[colIndex].textContent.trim().toLowerCase();
                            const aNum = parseFloat(aVal);
                            const bNum = parseFloat(bVal);
                            if (!isNaN(aNum) && !isNaN(bNum) && aVal !== '' && bVal !== '') {
                                return isDesc ? bNum - aNum : aNum - bNum;
                            }
                            return isDesc ? bVal.localeCompare(aVal) : aVal.localeCompare(bVal);
                        };
                    }
                    rows.sort(sortFn);
                    rows.forEach(row => tbody.appendChild(row));
                });
            });
        });

        // Popup de foto modularizado
        var popup = document.getElementById('image-popup');
        var popupImg = popup.querySelector('img');
        document.querySelectorAll('a.btnFoto').forEach(function(link) {
            link.addEventListener('mouseenter', function() {
                popupImg.src = link.getAttribute('href');
                popup.style.display = 'block';
                var rect = link.getBoundingClientRect();
                popup.style.top = (rect.bottom + window.scrollY - 122) + 'px';
                popup.style.left = (rect.left + window.scrollX + 70) + 'px';
            });
            link.addEventListener('mouseleave', function() {
                popup.style.display = 'none';
                popupImg.src = '';
            });
        });

        document.querySelectorAll('.rating').forEach(cell => {
                const stars = 5;
                let value = parseInt(cell.dataset.value) || 0;
                cell.innerHTML = '';
                for (let i = 1; i <= stars; i++) {
                    const star = document.createElement('span');
                    star.textContent = '★';
                    star.dataset.value = i;
                    star.style.cursor = 'pointer';
                    star.style.color = i <= value ? '#ffc107' : '#999';
                    star.addEventListener('mouseover', () => highlight(cell, i));
                    star.addEventListener('mouseout', () => highlight(cell, value));
                    star.addEventListener('click', () => {
                        value = i;
                        cell.dataset.value = value;
                        highlight(cell, value);
                        // AJAX para guardar calificación
                        fetch('/admin/calificar', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                id_postulante: cell.dataset.id,
                                calificacion: value
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                cell.title = 'Calificación guardada';
                            } else {
                                cell.title = 'Error al guardar';
                            }
                        })
                        .catch(() => {
                            cell.title = 'Error de conexión';
                        });
                    });
                    cell.appendChild(star);
                }
            });

            function highlight(cell, val) {
                const stars = cell.querySelectorAll('span');
                stars.forEach((star, index) => {
                    star.style.color = index < val ? '#ffc107' : '#999';
                });
            }

            // Ordenar por ID de a descendente al cargar la página
            document.addEventListener('DOMContentLoaded', function() {
                const tbody = document.querySelector('table tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                rows.sort((a, b) => {
                    const aId = parseInt(a.children[0].textContent) || 0;
                    const bId = parseInt(b.children[0].textContent) || 0;
                    return bId - aId;
                });
                rows.forEach(row => tbody.appendChild(row));
            });

            // Alternar orden ascendente/descendente solo en columnas 'sortable'
            let sortState = {};
            document.querySelectorAll('th.sortable').forEach(th => {
                th.addEventListener('click', function() {
                    const colIndex = parseInt(th.getAttribute('data-col'));
                    const tbody = th.closest('table').querySelector('tbody');
                    const rows = Array.from(tbody.querySelectorAll('tr'));

                    // Invert initial sort direction: first click is descending
                    if (sortState[colIndex] === undefined) {
                        sortState[colIndex] = true; // true = descending first
                    } else {
                        sortState[colIndex] = !sortState[colIndex];
                    }
                    const isDesc = sortState[colIndex];

                    let sortFn;
                    if (colIndex === 21) { // calificación
                        sortFn = (a, b) => {
                            const aVal = parseInt(a.querySelector('.rating').dataset.value) || 0;
                            const bVal = parseInt(b.querySelector('.rating').dataset.value) || 0;
                            return isDesc ? bVal - aVal : aVal - bVal;
                        };
                    } else {
                        sortFn = (a, b) => {
                            const aVal = a.children[colIndex].textContent.trim().toLowerCase();
                            const bVal = b.children[colIndex].textContent.trim().toLowerCase();
                            const aNum = parseFloat(aVal);
                            const bNum = parseFloat(bVal);
                            if (!isNaN(aNum) && !isNaN(bNum) && aVal !== '' && bVal !== '') {
                                return isDesc ? bNum - aNum : aNum - bNum;
                            }
                            return isDesc ? bVal.localeCompare(aVal) : aVal.localeCompare(bVal);
                        };
                    }
                    rows.sort(sortFn);
                    rows.forEach(row => tbody.appendChild(row));
                });
            });

        // Popup de previsualización de foto
        var popup = document.getElementById('image-popup');
        var popupImg = popup.querySelector('img');
        document.querySelectorAll('a.btnFoto').forEach(function(link) {
            link.addEventListener('mouseenter', function(e) {
                var imgSrc = link.getAttribute('href');
                popupImg.src = imgSrc;
                popup.style.display = 'block';
                var rect = link.getBoundingClientRect();
                popup.style.top = (rect.bottom + window.scrollY + 8 - 130) + 'px'; // Move popup 50px higher
                popup.style.left = (rect.left + window.scrollX+70) + 'px';
            });
            link.addEventListener('mouseleave', function() {
                popup.style.display = 'none';
                popupImg.src = '';
            });
        });