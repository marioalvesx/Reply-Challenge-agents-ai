# Reply Mirror - AI Agent Challenge 2026

Sistema multi-agente cooperativo para detecção de fraudes financeiras evolutivas.

## 📋 Visão Geral

Este projeto implementa um sistema baseado em agentes inteligentes para detectar fraudes financeiras que evoluem ao longo do tempo. O sistema utiliza múltiplos agentes especializados que trabalham cooperativamente, adaptando-se a novos padrões de fraude através de aprendizado contínuo.

## 🎯 Características Principais

- **Sistema Multi-Agente:** Agentes especializados em diferentes aspectos (transações, temporal, geoespacial, rede, comunicação)
- **Aprendizado Adaptativo:** Transfer learning entre níveis do desafio
- **Tracking Obrigatório:** Integração com Langfuse para monitoramento de custos
- **Custos Assimétricos:** Otimização considerando diferentes custos de falsos positivos vs negativos
- **Validação Rigorosa:** Validação temporal para evitar data leakage

## 🔧 Setup

### 1. Requisitos

- **Python 3.13** (RECOMENDADO - NÃO usar 3.14 por incompatibilidade com Langfuse)
- Credenciais Langfuse (fornecidas pelo desafio)
- OpenRouter API Key

### 2. Instalação

```bash
# Criar e ativar virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Atualizar pip e instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Download modelos NLP (opcional, se usar análise de comunicações)
python -m spacy download en_core_web_sm
```

### 3. Configuração

Criar arquivo `.env` na raiz do projeto (já existe):

```env
OPENROUTER_API_KEY=your-api-key-here
LANGFUSE_PUBLIC_KEY=pk-your-public-key-here
LANGFUSE_SECRET_KEY=sk-your-secret-key-here
LANGFUSE_HOST=https://challenges.reply.com/langfuse
TEAM_NAME=your-team-name
LANGFUSE_MEDIA_UPLOAD_ENABLED=false
```

### 4. Validar Setup

```bash
# Testar instalação e configuração
python test_setup.py

# Testar conexão e tracking Langfuse
python test_langfuse.py
```

## 🚀 Uso

### Estrutura de Comandos

```bash
# Treinar modelo (usando training dataset)
python main.py --level 1 --mode train --input data/raw/level1_train.csv

# Gerar predições (usando evaluation dataset)
python main.py --level 1 --mode predict --input data/raw/level1_eval.csv --output data/outputs/level1_output.txt

# Validar output antes de submeter
python main.py --mode validate --input data/outputs/level1_output.txt --total 10000
```

### Workflow por Nível

1. **Baixar datasets** do nível na plataforma Reply
2. **Colocar em `data/raw/`**: `levelN_train.csv`, `levelN_eval.csv`
3. **Treinar**: `python main.py --level N --mode train --input data/raw/levelN_train.csv`
4. **Prever**: `python main.py --level N --mode predict --input data/raw/levelN_eval.csv --output data/outputs/levelN_output.txt`
5. **Validar**: `python main.py --mode validate --input data/outputs/levelN_output.txt`
6. **Submeter** na plataforma Reply (⚠️ apenas 1 tentativa!)

## 📁 Estrutura do Projeto

```
Reply Challenge/
├── .env                          # Credenciais (não commitar!)
├── requirements.txt              # Dependências Python
├── config.yaml                   # Configurações do sistema
├── README.md                     # Este arquivo
├── main.py                       # Ponto de entrada principal
├── test_setup.py                 # Validação de setup
├── test_langfuse.py              # Teste de tracking
│
├── agents/                       # Agentes especializados
│   ├── orchestrator.py           # Agente coordenador
│   ├── transaction_agent.py      # Análise de padrões transacionais
│   ├── temporal_agent.py         # Análise temporal
│   ├── geospatial_agent.py       # Análise geoespacial
│   ├── network_agent.py          # Análise de rede/grafos
│   └── communication_agent.py    # Análise de comunicações (NLP)
│
├── features/                     # Feature engineering
│   └── engineering.py            # Pipeline de features
│
├── models/                       # Modelos e ensemble
│   └── ensemble.py               # Ensemble de modelos
│
├── utils/                        # Utilidades
│   ├── langfuse_tracking.py      # Sistema de tracking (OBRIGATÓRIO)
│   ├── validation.py             # Validação de outputs
│   └── metrics.py                # Métricas customizadas
│
├── data/                         # Datasets
│   ├── raw/                      # Dados originais
│   ├── processed/                # Dados processados
│   └── outputs/                  # Outputs para submissão
│
└── tests/                        # Testes
```

## 📊 Datasets

### Arquivos de Input

- **Transactions.csv**: Dataset principal com transações
- **Locations.csv**: Dados de GPS dos cidadãos
- **Users.csv**: Dados demográficos
- **Conversations.csv**: Threads de SMS
- **Messages.csv**: Threads de e-mail

### Formato de Output

Arquivo ASCII text com Transaction IDs suspeitos (um por linha):

```
4a92ab00-8a27-4623-ab1d-56ac85fcd6b0
8830a720-ff34-4dce-a578-e5b8006b2976
```

## ⚠️ Regras Críticas

### OBRIGATÓRIO

- ✅ Sistema baseado em agentes (agent-based)
- ✅ Langfuse tracking em todas as chamadas LLM
- ✅ Apenas 1 submissão por nível (primeira é final!)
- ✅ Detectar mínimo 15% das fraudes
- ✅ Não reportar 0% ou 100% das transações

### PENALIZADO

- ❌ Abordagens totalmente determinísticas
- ❌ Usar Python 3.14 (incompatível com Langfuse)
- ❌ Usar Langfuse v4 (não suportado - usar v3)

## 🎯 Sistema de Agentes

### Agente Coordenador (Orchestrator)

- Gerencia fluxo entre agentes especializados
- Agrega scores de risco
- Mantém memória de padrões históricos

### Agentes Especializados

- **Transaction Pattern Agent**: Analisa valores, frequências, sequências
- **Temporal Behavior Agent**: Detecta anomalias temporais
- **Geospatial Agent**: Correlaciona transações com GPS
- **Network Analysis Agent**: Analisa grafos de relacionamentos
- **Communication Agent**: Processa SMS/emails (NLP)

## 📈 Métricas de Avaliação

### Principal: Accuracy

- Balance entre detectar fraudes vs evitar falsos positivos
- Considera custos assimétricos (FP vs FN)

### Complementares

- **Custo Operacional**: Eficiência de recursos
- **Velocidade**: Latência de processamento
- **Eficiência**: Escalabilidade da arquitetura

## 🔄 Adaptação entre Níveis

1. Análise de performance do nível anterior
2. Detecção de drift de padrões
3. Transfer learning (reutilizar features/pesos)
4. Ajuste de thresholds
5. Otimização de custos

## 🛠️ Dependências Principais

- **LangChain + Langfuse**: Tracking obrigatório (v3)
- **XGBoost, LightGBM, CatBoost**: Modelos de ML
- **NetworkX**: Análise de grafos
- **GeoPandas**: Análise geoespacial
- **spaCy**: NLP para comunicações
- **LangGraph**: Framework multi-agente

## 📚 Recursos

- [Langfuse Documentation](https://langfuse.com/docs)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [API Guidelines](https://cdn.reply.com/documents/challenges/02_26/api_guidelines.html)

## 🐛 Troubleshooting

### Erro: "Langfuse v4 not supported"

```bash
pip uninstall langfuse
pip install "langfuse>=3.0.0,<4.0.0"
```

### Erro: "Session ID contains spaces"

- Verificar que `generate_session_id()` usa `.replace(" ", "-")`

### Erro: "Langfuse connection failed"

- Verificar credenciais no `.env`
- Verificar LANGFUSE_HOST correto
- Testar conexão: `python test_langfuse.py`

## 📝 Notas Importantes

- **Top teams** podem ser reavaliados em novos datasets
- Sistema deve **generalizar**, não overfit
- Priorizar **robustez** sobre accuracy máxima
- **Documentar decisões** de design

## 👥 Equipe

Team Name: mario-e-matheus-933e-team

---

**Boa sorte no desafio! 🚀**
