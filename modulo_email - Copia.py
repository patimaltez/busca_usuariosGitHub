import win32com.client
import traceback

def enviar_email(assunto, corpo, destinatario="email_destinatario@gmail.com"):
    """
    Envia um email usando o Outlook configurado no sistema.
    
    :param assunto: Assunto do email.
    :param corpo: Corpo do email.
    :param destinatario: Endereço de email do destinatário.
    """
    try:
        # Conecta ao Outlook
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)  # 0 indica um email
        
        # Configura o email
        mail.To = destinatario
        mail.Subject = assunto
        mail.Body = corpo
        
        # Envia o email
        mail.Send()
        print("[informação] Email enviado com sucesso.")
    except Exception as e:
        print(f"[ERRO] Falha ao enviar email: {e}")
        traceback.print_exc()