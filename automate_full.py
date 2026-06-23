import asyncio
from playwright.async_api import async_playwright
import os

async def run_scenario(scenario_name, responses):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # 1. Acessar a calculadora local
        calc_path = "file://" + os.path.abspath("index.html")
        print(f"\n--- Iniciando Cenário: {scenario_name} ---")
        await page.goto(calc_path)

        # 2. Preencher a calculadora
        for i, val in enumerate(responses, 1):
            await page.wait_for_selector(f'#step-{i}.active')
            await page.check(f'#step-{i} input[value="{val}"]')
            if i < 4:
                await page.click(f'#step-{i} .btn-next')
            else:
                await page.click('button:has-text("Ver Resultado")')

        # 3. Aguardar redirecionamento
        print("Aguardando redirecionamento...")
        await page.wait_for_url("**/forms.cloud.microsoft/**", timeout=15000)
        
        # 4. No Microsoft Forms
        print(f"Formulário carregado para {scenario_name}. Verificando e enviando...")
        await page.wait_for_selector('button:has-text("Submit")')
        
        # O pre-fill deve selecionar automaticamente, mas vamos garantir o clique na opção correta
        await page.click(f'span:has-text("{scenario_name}")')
        
        # Clicar em Enviar
        await page.click('button:has-text("Submit")')
        print(f"Enviado com sucesso: {scenario_name}")

        await browser.close()

async def main():
    # Cenários de teste: [q1, q2, q3, q4]
    scenarios = {
        "Pegada Ecológica Baixa": ["0", "5", "5", "0"],
        "Pegada Ecológica Moderada": ["30", "20", "15", "15"],
        "Pegada Ecológica Alta": ["50", "40", "35", "30"]
    }
    
    for name, resp in scenarios.items():
        try:
            await run_scenario(name, resp)
        except Exception as e:
            print(f"Erro no cenário {name}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
