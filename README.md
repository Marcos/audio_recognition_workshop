# Sistema de Menu por Voz

Este projeto implementa um sistema de menu interativo por voz utilizando os serviços de fala da Azure. O sistema permite que os usuários interajam com um menu de opções através de comandos de voz, oferecendo uma experiência natural e acessível.

## Funcionalidades

- Text-to-Speech (TTS): Converte texto em fala natural
- Speech-to-Text (STT): Reconhece comandos de voz do usuário
- Menu interativo com 4 opções:
  1. Consulta ao saldo da conta
  2. Simulação de compra internacional
  3. Falar com um atendente
  4. Sair do atendimento

## Requisitos

- Python 3.x
- Microfone funcional
- Conta Azure com serviço de fala ativado
- Dependências listadas em `requirements.txt`

## Configuração

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Crie um arquivo `.env` na raiz do projeto com suas credenciais Azure:
   ```
   AZURE_SPEECH_KEY=sua_chave_aqui
   AZURE_SPEECH_REGION=sua_regiao_aqui
   ```

## Como Usar

Execute o script principal:
```bash
python voice_menu.py
```

O sistema irá:
1. Apresentar uma mensagem de boas-vindas
2. Listar as opções disponíveis
3. Aguardar o comando de voz do usuário
4. Confirmar a opção selecionada
5. Repetir o processo até que o usuário escolha sair

## Estrutura do Código

### Componentes Principais

- `text_to_speech()`: Converte texto em fala usando o serviço TTS da Azure
- `speech_to_text()`: Captura e converte fala em texto usando o serviço STT da Azure
- `identify_option()`: Identifica a opção selecionada através de palavras-chave
- `play_menu()`: Apresenta as opções disponíveis
- `main()`: Loop principal do sistema

### Reconhecimento de Comandos

O sistema identifica as opções através de palavras-chave:
- Opção 1: "saldo" ou "conta"
- Opção 2: "compra" ou "internacional"
- Opção 3: "atendente" ou "humano"
- Opção 4: "sair" ou "encerrar"
