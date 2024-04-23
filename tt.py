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

def get_profissional(id):
    profissionais = load_agenda().get('profissionais')
    if profissionais:
        for p  in profissionais:
            if p['id'] == int(id):
                return p
    return profissionais

def list_available_slots(id_prof):
    agenda = load_agenda().get('agenda_medico', {})
    available_slots = []
    for slot_id, slot_info in agenda.items():
        if not slot_info.get('paciente') and not slot_info.get('reservado') and slot_info.get('profissional') == int(id_prof):
            available_slots.append({'id': slot_id, 'date': slot_info['data'], 'time': slot_info['hora']})
    
    profissional = get_profissional(id_prof)
    if available_slots:
            response_message = f"Datas e horários disponíveis para marcar uma consulta com {profissional['nome']} - {profissional['especialidade']}:\nResponda com o 'ID da consulta disponível-Seu nome-Seu CPF-Seu sintomas' para marcar consulta ou digite 'Oi' para voltar o menu \n"
            for slot in available_slots:
                response_message += f"ID: {slot['id']}, Data: {slot['date']}, Hora: {slot['time']}\n"
            return response_message

def marcar():
    parts='8-Miguel-00000-uiuiui'
    parts = parts.upper().split('-')
    if len(parts) == 4:
        appointment_id, user_name, user_cpf, user_symptoms = parts[0], parts[1], parts[2], parts[3]
        agenda = load_agenda()
        if appointment_id in agenda['agenda_medico']:
            print(appointment_id)
            appointment_info = agenda['agenda_medico'][appointment_id]
            print(appointment_info)
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


def list_profissionais():
    profissionais = load_agenda().get('profissionais')
    return profissionais

def teste_list():
    response_message = "Estes são nossos profissionais:\nPara consultar Datas e horários disponíveis digite 'agendar:ID do medico' \n"
    for prof in list_profissionais():
        response_message += f"ID: {prof['id']}, Nome: {prof['nome']}, Especialidade: {prof['especialidade']}\n"
    return response_message


# print(list_profissionais())

print(teste_list())

print(list_available_slots('3'))


# print(marcar())
# mb = 'agendar:1'
# msg = mb.split(':')
# if 'agendar' in mb:
#     print(list_available_slots(msg[1]))
# elif '-' in mb:
#     print('marcar consulta')