// Cambia esta constante si el backend corre en otra URL/puerto.
  const API_BASE = "http://localhost:8000";
  document.getElementById("apiBase").textContent = API_BASE;

  const ESTADOS = ["Pendiente", "Aprobada", "Rechazada", "Finalizada"];

  const fmtFecha = (iso) => {
    try {
      const d = new Date(iso);
      return d.toLocaleString("es-MX", { day:"2-digit", month:"short", year:"numeric", hour:"2-digit", minute:"2-digit" });
    } catch { return iso; }
  };

  function showMsg(el, text, isError){
    el.textContent = text;
    el.className = "msg show " + (isError ? "err" : "ok");
    setTimeout(() => el.classList.remove("show"), 4000);
  }

  async function checkConexion(){
    const dot = document.getElementById("statusDot");
    const txt = document.getElementById("statusText");
    try{
      const res = await fetch(`${API_BASE}/`);
      if(!res.ok) throw new Error();
      dot.classList.add("on");
      txt.textContent = "Conectado a la API";
    }catch{
      dot.classList.remove("on");
      txt.textContent = "Sin conexión con la API — inícia el backend con: python main.py";
    }
  }

  // ---------------- Usuarios ----------------

  async function cargarUsuarios(){
    const tbody = document.getElementById("tablaUsuarios");
    const select = document.getElementById("s_usuario");
    try{
      const res = await fetch(`${API_BASE}/usuarios`);
      if(!res.ok) throw new Error();
      const usuarios = await res.json();

      if(usuarios.length === 0){
        tbody.innerHTML = `<tr><td class="empty" colspan="5">Todavía no hay usuarios registrados.</td></tr>`;
      }else{
        tbody.innerHTML = usuarios.map(u => `
          <tr>
            <td class="id">#${u.id}</td>
            <td>${escapeHtml(u.nombre)}</td>
            <td>${escapeHtml(u.email)}</td>
            <td><span class="role-pill">${escapeHtml(u.rol)}</span></td>
            <td class="date">${fmtFecha(u.fecha_creacion)}</td>
          </tr>
        `).join("");
      }

      const seleccionActual = select.value;
      select.innerHTML = `<option value="" disabled ${!seleccionActual ? "selected" : ""}>Selecciona un usuario…</option>` +
        usuarios.map(u => `<option value="${u.id}">${escapeHtml(u.nombre)} — ${escapeHtml(u.rol)}</option>`).join("");
      if(seleccionActual) select.value = seleccionActual;

    }catch{
      tbody.innerHTML = `<tr><td class="empty" colspan="5">No se pudo cargar el listado. Verifica que la API esté corriendo.</td></tr>`;
    }
  }

  document.getElementById("formUsuario").addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = e.target.querySelector("button");
    const msg = document.getElementById("u_msg");
    const payload = {
      nombre: document.getElementById("u_nombre").value.trim(),
      email: document.getElementById("u_email").value.trim(),
      rol: document.getElementById("u_rol").value,
    };
    btn.disabled = true;
    try{
      const res = await fetch(`${API_BASE}/usuarios`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if(!res.ok) throw new Error(data.detail || "No se pudo crear el usuario.");
      showMsg(msg, `Usuario #${data.id} registrado correctamente.`, false);
      e.target.reset();
      document.getElementById("u_rol").value = "Empleado";
      await cargarUsuarios();
    }catch(err){
      showMsg(msg, err.message, true);
    }finally{
      btn.disabled = false;
    }
  });

  // ---------------- Solicitudes ----------------

  async function cargarSolicitudes(){
    const tbody = document.getElementById("tablaSolicitudes");
    try{
      const res = await fetch(`${API_BASE}/solicitudes`);
      if(!res.ok) throw new Error();
      const solicitudes = await res.json();

      if(solicitudes.length === 0){
        tbody.innerHTML = `<tr><td class="empty" colspan="6">Todavía no hay solicitudes registradas.</td></tr>`;
        return;
      }

      tbody.innerHTML = solicitudes.map(s => `
        <tr>
          <td class="id">#${s.id}</td>
          <td>${escapeHtml(s.usuario_nombre || "—")}</td>
          <td>${escapeHtml(s.tipo)}</td>
          <td>${escapeHtml(s.descripcion || "—")}</td>
          <td>
            <select class="estado-select estado-${s.estado}" data-id="${s.id}">
              ${ESTADOS.map(es => `<option value="${es}" ${es === s.estado ? "selected" : ""}>${es}</option>`).join("")}
            </select>
          </td>
          <td class="date">${fmtFecha(s.fecha_creacion)}</td>
        </tr>
      `).join("");

      tbody.querySelectorAll(".estado-select").forEach(sel => {
        sel.addEventListener("change", () => actualizarEstado(sel));
      });

    }catch{
      tbody.innerHTML = `<tr><td class="empty" colspan="6">No se pudo cargar el historial. Verifica que la API esté corriendo.</td></tr>`;
    }
  }

  async function actualizarEstado(selectEl){
    const id = selectEl.dataset.id;
    const nuevoEstado = selectEl.value;
    selectEl.disabled = true;
    try{
      const res = await fetch(`${API_BASE}/solicitudes/${id}/estado`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ estado: nuevoEstado }),
      });
      if(!res.ok) throw new Error();
      selectEl.className = `estado-select estado-${nuevoEstado}`;
    }catch{
      alert("No se pudo actualizar el estado de la solicitud.");
      await cargarSolicitudes();
    }finally{
      selectEl.disabled = false;
    }
  }

  document.getElementById("formSolicitud").addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = e.target.querySelector("button");
    const msg = document.getElementById("s_msg");
    const payload = {
      usuario_id: Number(document.getElementById("s_usuario").value),
      tipo: document.getElementById("s_tipo").value,
      descripcion: document.getElementById("s_desc").value.trim(),
    };
    if(!payload.usuario_id){
      showMsg(msg, "Selecciona primero un usuario.", true);
      return;
    }
    btn.disabled = true;
    try{
      const res = await fetch(`${API_BASE}/solicitudes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if(!res.ok) throw new Error(data.detail || "No se pudo crear la solicitud.");
      showMsg(msg, `Solicitud #${data.id} registrada correctamente.`, false);
      document.getElementById("s_desc").value = "";
      await cargarSolicitudes();
    }catch(err){
      showMsg(msg, err.message, true);
    }finally{
      btn.disabled = false;
    }
  });

  function escapeHtml(str){
    return String(str).replace(/[&<>"']/g, (c) => ({
      "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"
    }[c]));
  }

  // ---------------- Carga inicial ----------------
  (async function init(){
    await checkConexion();
    await cargarUsuarios();
    await cargarSolicitudes();
  })();
