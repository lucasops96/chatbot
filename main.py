from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

JSON_FILE = 'dados.json'

def load_agenda():
    try:
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_agenda(agenda):
    with open(JSON_FILE, 'w') as f:
        json.dump(agenda, f, indent=2)

def list_available_slots():
    agenda = load_agenda().get('agenda_medico', {})
    available_slots = []
    for slot_id, slot_info in agenda.items():
        if not slot_info.get('paciente') and not slot_info.get('reservado'):
            available_slots.append({'id': slot_id, 'date': slot_info['data'], 'time': slot_info['hora']})
    return available_slots

def process_message(userid,msg_body):
    
    if 'oi' in msg_body:
        return ("Olá! Como posso ajudar? \n"
                "1. Marcar uma consulta \n"
                "2. Relatar sintomas")
    
    elif '1' == msg_body:
        available_slots = list_available_slots()
        if available_slots:
            response_message = "Datas e horários disponíveis para marcar uma consulta:\n \
                                Responda com o 'ID da consulta disponível-Seu nome-Seu CPF-Seu sintomas' para marcar consulta ou digite 'Oi' para voltar o menu \n"
            for slot in available_slots:
                response_message += f"ID: {slot['id']}, Data: {slot['date']}, Hora: {slot['time']}\n"
            return response_message
        else:
            return "Desculpe, não há datas e horários disponíveis para marcar uma consulta no momento."
    
    elif '2' == msg_body:
        return "Por favor, descreva seus sintomas para que eu possa ajudar a avaliar sua situação."
    
    elif '-' in msg_body:
        parts = msg_body.upper().split('-')
        if len(parts) == 4:
            appointment_id, user_name, user_cpf, user_symptoms = parts[0], parts[1], parts[2], parts[3]
            agenda = load_agenda()
            if appointment_id in agenda['agenda_medico']:
                appointment_info = agenda['agenda_medico'][appointment_id]
                if not appointment_info.get('reservado') and not appointment_info.get('paciente'):
                    
                    appointment_info['paciente'] = {
                        'id': userid,
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
                else:
                    return "Desculpe, este horário já está reservado para outra consulta."
            else:
                return "ID de consulta inválido."
        else:
            return "Formato inválido. Por favor, responda com o ID seguido pelo seu nome, CPF e sintomas para marcar a consulta."
    
    else:
        return "Desculpe, não entendi. Por favor, escolha uma das opções fornecidas."


@app.route('/bot',methods=['POST'])
def bot():
    print(request.values)
    
    msg_body = request.values.get('Body','').lower()

    userid = request.values.get('WaId', None)

    response_message = process_message(userid,msg_body)

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(response_message)

    print(resp)
    return str(resp)

@app.route('/')
def index():
    return 'Tá funcionando o Flask'


if __name__ == '__main__':
    app.run()