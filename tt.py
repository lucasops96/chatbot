import json
JSON_FILE = 'dados.json'

def load_agenda():
    try:
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Se o arquivo não existir, retorna um dicionário vazio
        return {}

def save_agenda(agenda):
    with open(JSON_FILE, 'w') as f:
        json.dump(agenda, f, indent=2)

def list_available_slots():
    agenda = load_agenda().get('agenda_medico', {})
    available_slots = []
    for slot_id, slot_info in agenda.items():
        print(slot_id)
        print(slot_info)
        if not slot_info.get('paciente') and not slot_info.get('reservado'):
            available_slots.append({'id': slot_id, 'date': slot_info['data'], 'time': slot_info['hora']})
    return available_slots

def marcar():
    parts='5-Miguel-00000-uiuiui'
    parts = parts.upper().split('-')
    if len(parts) == 4:
        appointment_id, user_name, user_cpf, user_symptoms = parts[0], parts[1], parts[2], parts[3]
        agenda = load_agenda()
        if appointment_id in agenda['agenda_medico']:
            appointment_info = agenda['agenda_medico'][appointment_id]
            if not appointment_info.get('reservado') and not appointment_info.get('paciente'):
                # Marcar consulta
                appointment_info['paciente'] = {
                    'id': '242389748',
                    'nome': user_name,
                    'cpf': user_cpf,
                    'sintomas': user_symptoms
                }
                appointment_info['reservado'] = True
                save_agenda(agenda)
                return f"Consulta marcada com sucesso para {user_name}.\n\
                        Data e hora: {appointment_info['data']} - {appointment_info['hora']}\n\
                        CPF: {user_cpf}\n\
                        Sintomas: {user_symptoms}"

print(marcar())