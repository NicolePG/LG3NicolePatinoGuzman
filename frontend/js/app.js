const api = {
  async request(url, options = {}) {
    const response = await fetch(url, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.detail || 'Ocurrió un error en la solicitud.');
    }
    return data;
  },
  listGroups() { return this.request('/api/groups'); },
  createGroup(payload) { return this.request('/api/groups', { method: 'POST', body: JSON.stringify(payload) }); },
  updateGroup(code, payload) { return this.request(`/api/groups/${code}`, { method: 'PUT', body: JSON.stringify(payload) }); },
  listPersons() { return this.request('/api/persons'); },
  createPerson(payload) { return this.request('/api/persons', { method: 'POST', body: JSON.stringify(payload) }); },
  updatePerson(code, payload) { return this.request(`/api/persons/${code}`, { method: 'PUT', body: JSON.stringify(payload) }); },
};

const state = {
  groups: [],
  persons: [],
  currentPhotoBase64: null,
};

const groupForm = document.getElementById('groupForm');
const personForm = document.getElementById('personForm');
const groupList = document.getElementById('groupList');
const personList = document.getElementById('personList');
const groupSelect = document.getElementById('groupSelect');
const photoInput = document.getElementById('photo');
const photoPreview = document.getElementById('photoPreview');
const toast = document.getElementById('toast');

function notify(message) {
  toast.textContent = message;
  toast.classList.remove('hidden');
  setTimeout(() => toast.classList.add('hidden'), 2500);
}

function statusBadge(value) {
  return `<span class="status ${value ? 'active' : 'inactive'}">${value ? 'Activo' : 'Inactivo'}</span>`;
}

function fillGroupSelect() {
  groupSelect.innerHTML = '';
  if (state.groups.length === 0) {
    const option = document.createElement('option');
    option.value = '';
    option.textContent = 'Primero registra un grupo';
    groupSelect.appendChild(option);
    return;
  }
  for (const group of state.groups) {
    const option = document.createElement('option');
    option.value = group.code;
    option.textContent = `${group.group} (${group.is_active ? 'Activo' : 'Inactivo'})`;
    groupSelect.appendChild(option);
  }
}

function renderGroups() {
  document.getElementById('groupCounter').textContent = `${state.groups.length} grupo(s)`;
  groupList.innerHTML = state.groups.map(group => `
    <article class="group-row">
      <div>
        <strong>${group.group}</strong>
        <small>UUID: ${group.code}</small>
        <small>Personas asociadas: ${group.people_count}</small>
      </div>
      <div class="card-actions">
        ${statusBadge(group.is_active)}
        <button class="edit-btn" type="button" onclick="editGroup('${group.code}')">Editar</button>
      </div>
    </article>
  `).join('') || '<p class="meta">Aún no hay grupos registrados.</p>';
}

function renderPersons() {
  document.getElementById('personCounter').textContent = `${state.persons.length} persona(s)`;
  personList.innerHTML = state.persons.map(person => `
    <article class="person-card">
      <img src="${person.photo_base64 || 'https://placehold.co/600x400?text=Sin+foto'}" alt="${person.names} ${person.last_names}" />
      <div class="person-card-content">
        <div class="card-actions">
          <h3>${person.names} ${person.last_names}</h3>
          ${statusBadge(person.is_active)}
        </div>
        <div class="meta">Grupo: ${person.group_name}</div>
        <div class="meta">Correo: ${person.email}</div>
        <div class="meta">Celular: ${person.cell_number}</div>
        <div class="meta">Dirección: ${person.address}</div>
        <div class="meta">UUID: ${person.code}</div>
        <div class="observations">${person.observations || 'Sin observaciones.'}</div>
        <div class="card-actions">
          <span class="meta">${person.group_name}</span>
          <button class="edit-btn" type="button" onclick="editPerson('${person.code}')">Editar</button>
        </div>
      </div>
    </article>
  `).join('') || '<p class="meta">Aún no hay personas registradas.</p>';
}

function resetGroupForm() {
  document.getElementById('groupCode').value = '';
  document.getElementById('groupName').value = '';
  document.getElementById('groupActive').checked = true;
}

function resetPersonForm() {
  document.getElementById('personCode').value = '';
  document.getElementById('names').value = '';
  document.getElementById('lastNames').value = '';
  document.getElementById('email').value = '';
  document.getElementById('cellNumber').value = '';
  document.getElementById('address').value = '';
  document.getElementById('observations').value = '';
  document.getElementById('personActive').checked = true;
  state.currentPhotoBase64 = null;
  photoInput.value = '';
  photoPreview.src = '';
  if (state.groups.length > 0) groupSelect.value = state.groups[0].code;
}

window.editGroup = function (code) {
  const group = state.groups.find(g => g.code === code);
  if (!group) return;
  document.getElementById('groupCode').value = group.code;
  document.getElementById('groupName').value = group.group;
  document.getElementById('groupActive').checked = group.is_active;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

window.editPerson = function (code) {
  const person = state.persons.find(p => p.code === code);
  if (!person) return;
  document.getElementById('personCode').value = person.code;
  document.getElementById('names').value = person.names;
  document.getElementById('lastNames').value = person.last_names;
  document.getElementById('email').value = person.email;
  document.getElementById('cellNumber').value = person.cell_number;
  document.getElementById('address').value = person.address;
  document.getElementById('observations').value = person.observations || '';
  document.getElementById('personActive').checked = person.is_active;
  groupSelect.value = person.group_code;
  state.currentPhotoBase64 = person.photo_base64 || null;
  photoPreview.src = person.photo_base64 || '';
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

photoInput.addEventListener('change', async (event) => {
  const file = event.target.files?.[0];
  if (!file) {
    state.currentPhotoBase64 = null;
    photoPreview.src = '';
    return;
  }

  const reader = new FileReader();
  reader.onload = () => {
    state.currentPhotoBase64 = reader.result;
    photoPreview.src = reader.result;
  };
  reader.readAsDataURL(file);
});

groupForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    const code = document.getElementById('groupCode').value;
    const payload = {
      group: document.getElementById('groupName').value.trim(),
      is_active: document.getElementById('groupActive').checked,
    };

    if (code) {
      await api.updateGroup(code, payload);
      notify('Grupo actualizado correctamente.');
    } else {
      await api.createGroup(payload);
      notify('Grupo creado correctamente.');
    }

    resetGroupForm();
    await loadAll();
  } catch (error) {
    notify(error.message);
  }
});

personForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    const code = document.getElementById('personCode').value;
    const payload = {
      names: document.getElementById('names').value.trim(),
      last_names: document.getElementById('lastNames').value.trim(),
      email: document.getElementById('email').value.trim(),
      cell_number: document.getElementById('cellNumber').value.trim(),
      address: document.getElementById('address').value.trim(),
      observations: document.getElementById('observations').value.trim(),
      photo_base64: state.currentPhotoBase64,
      is_active: document.getElementById('personActive').checked,
      group_code: document.getElementById('groupSelect').value,
    };

    if (!payload.group_code) {
      notify('Primero debes registrar un grupo.');
      return;
    }

    if (code) {
      await api.updatePerson(code, payload);
      notify('Persona actualizada correctamente.');
    } else {
      await api.createPerson(payload);
      notify('Persona registrada correctamente.');
    }

    resetPersonForm();
    await loadAll();
  } catch (error) {
    notify(error.message);
  }
});

async function loadAll() {
  const [groups, persons] = await Promise.all([api.listGroups(), api.listPersons()]);
  state.groups = groups;
  state.persons = persons;
  fillGroupSelect();
  renderGroups();
  renderPersons();
}

document.getElementById('resetGroupBtn').addEventListener('click', resetGroupForm);
document.getElementById('resetPersonBtn').addEventListener('click', resetPersonForm);

loadAll().catch(error => notify(error.message));
