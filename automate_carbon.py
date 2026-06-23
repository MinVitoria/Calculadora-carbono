import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        # Abre o navegador
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # 1. Acessar a calculadora local
        calc_path = "file://" + os.path.abspath("calculadora_carbono.html")
        print(f"Acessando a calculadora em: {calc_path}")
        await page.goto(calc_path)

        # 2. Preencher a calculadora para dar "Pegada Alta"
        # Passo 1: De Carro (50)
        print("Passo 1: Selecionando transporte...")
        await page.wait_for_selector('#step-1.active')
        await page.check('#step-1 input[value="50"]')
        await page.click('#step-1 .btn-next')

        # Passo 2: Quase todos os dias (40)
        print("Passo 2: Selecionando consumo de carne...")
        await page.wait_for_selector('#step-2.active')
        await page.check('#step-2 input[value="40"]')
        await page.click('#step-2 .btn-next')

        # Passo 3: Mais de 15 minutos (35)
        print("Passo 3: Selecionando tempo de banho...")
        await page.wait_for_selector('#step-3.active')
        await page.check('#step-3 input[value="35"]')
        await page.click('#step-3 .btn-next')

        # Passo 4: Não, misturamos todo o lixo (30)
        print("Passo 4: Selecionando reciclagem...")
        await page.wait_for_selector('#step-4.active')
        await page.check('#step-4 input[value="30"]')
        
        # Ver Resultado
        print("Calculando resultado...")
        await page.click('#step-4 button:has-text("Ver Resultado")')

        # Esperar o redirecionamento automático
        print("Aguardando redirecionamento para o Microsoft Forms...")
        # O redirecionamento leva 3 segundos no script HTML
        await page.wait_for_url("**/forms.cloud.microsoft/**", timeout=15000)
        
        # 3. No Microsoft Forms
        print("Formulário carregado. Verificando seleção e enviando...")
        
        # Aguarda o formulário carregar os elementos principais
        await page.wait_for_selector('button:has-text("Submit")')
        
        # Garantir que a opção correta está selecionada (o pre-fill deve ter feito isso)
        # Se não estiver, clicamos explicitamente
        await page.click('span:has-text("Pegada Ecológica Alta")')
        
        print("Clicando em Enviar (Submit)...")
        await page.click('button:has-text("Submit")')

        # Esperar confirmação de envio
        try:
            await page.wait_for_selector('text="Your response was submitted"', timeout=10000)
            print("Sucesso! O formulário foi enviado com Pegada Ecológica Alta.")
        except:
            print("Aviso: Não foi possível confirmar a mensagem de sucesso, mas o clique em enviar foi realizado.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
