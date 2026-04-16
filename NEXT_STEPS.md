# Próximos Passos - Implementação Completa

## ✅ Setup Concluído!

Estrutura de projeto criada com sucesso! Agora siga estes passos:

---

## 🔧 1. Instalar Dependências

Abra um terminal no diretório do projeto e execute:

```bash
# Criar virtual environment
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
# source venv/bin/activate

# Atualizar pip
python -m pip install --upgrade pip

# Instalar todas as dependências
pip install -r requirements.txt
```

**IMPORTANTE:** Este passo pode demorar alguns minutos. O PyTorch é grande (~2GB).

---

## ✅ 2. Validar Setup

Após instalar as dependências, validar que tudo está correto:

```bash
# Testar instalação e configuração
python test_setup.py
```

**Esperado:** Todos os testes devem passar (✅). Se algum falhar, revisar mensagens de erro.

---

## 🔍 3. Testar Tracking Langfuse

Validar que o sistema de tracking (OBRIGATÓRIO) está funcionando:

```bash
python test_langfuse.py
```

**Esperado:**

- ✅ LLM call bem-sucedido
- ✅ Traces enviados para Langfuse
- Session ID no formato: `mario-e-matheus-933e-team-ULID`

Depois, verificar no dashboard Langfuse:

- URL: https://challenges.reply.com/langfuse
- Buscar pelo Session ID
- Confirmar que tokens e custos foram rastreados

---

## 📊 4. Baixar Datasets do Nível 1

1. Acessar plataforma Reply Challenges
2. Baixar datasets do Nível 1:
   - `Transactions.csv` (treino)
   - `Transactions.csv` (avaliação)
   - Datasets auxiliares (Locations, Users, Conversations, Messages)

3. Colocar em `data/raw/`:
   ```
   data/raw/
   ├── level1_train_transactions.csv
   ├── level1_eval_transactions.csv
   ├── level1_locations.csv
   ├── level1_users.csv
   ├── level1_conversations.csv
   └── level1_messages.csv
   ```

---

## 🔬 5. Fazer EDA (Exploração de Dados)

Criar um notebook ou script para entender os dados:

```python
import pandas as pd

# Carregar dados
transactions = pd.read_csv('data/raw/level1_train_transactions.csv')

# Explorar
print(transactions.head())
print(transactions.info())
print(transactions.describe())

# Verificar taxa de fraude (se houver label)
if 'is_fraud' in transactions.columns:
    fraud_rate = transactions['is_fraud'].mean()
    print(f"Fraud rate: {fraud_rate:.2%}")

# Analisar distribuições
# - Por tipo de transação
# - Por horário
# - Por valores
# - etc.
```

**Objetivos:**

- Entender estrutura dos dados
- Identificar missing values
- Analisar distribuição de fraudes
- Descobrir padrões iniciais

---

## 🚀 6. Implementar Pipeline de Treino

Os arquivos base já existem, mas precisam ser completados (marcados com TODO).

**Ordem de implementação:**

### A. Feature Engineering (`features/engineering.py`)

- Completar `create_aggregation_features()`
- Completar `create_user_deviation_features()`
- Completar `create_network_features()`
- Completar `create_geospatial_features()`
- Testar com dados reais

### B. Agentes (`agents/`)

- Completar `build_user_profile()` em cada agente
- Implementar `predict()` com lógica real
- Testar cada agente individualmente

### C. Ensemble (`models/ensemble.py`)

- Adicionar handling de class imbalance (SMOTE)
- Implementar `get_feature_importance()`
- Testar treino com dados sintéticos primeiro

### D. Main Pipeline (`main.py`)

- Implementar `train_mode()`:
  1. Carregar todos os datasets
  2. Executar feature engineering
  3. Treinar modelos
  4. Otimizar threshold
  5. Salvar modelos treinados

- Implementar `predict_mode()`:
  1. Carregar modelos salvos
  2. Carregar dados de avaliação
  3. Gerar predições
  4. Salvar output no formato correto

---

## 📝 7. Workflow de Desenvolvimento

Para cada nível do desafio:

```bash
# 1. Treinar com training dataset
python main.py --level 1 --mode train --input data/raw/level1_train_transactions.csv

# 2. Validar em local (se tiver labels)
# Fazer cross-validation temporal

# 3. Gerar predições para evaluation dataset
python main.py --level 1 --mode predict \
  --input data/raw/level1_eval_transactions.csv \
  --output data/outputs/level1_output.txt

# 4. Validar formato antes de submeter
python main.py --mode validate \
  --input data/outputs/level1_output.txt \
  --total <número_total_de_transações>

# 5. Submeter na plataforma Reply (apenas 1 tentativa!)
```

---

## ⚠️ Checklist Pré-Submissão

Antes de submeter cada nível:

- [ ] Output no formato ASCII correto (IDs em linhas)
- [ ] Output não está vazio (> 0% reportado)
- [ ] Output não contém todas transações (< 100%)
- [ ] Validação local passa (se tiver ground truth)
- [ ] Código está documentado
- [ ] requirements.txt atualizado
- [ ] README atualizado com instruções

---

## 🎯 Prioridades de Implementação

### Fase 1 (Mínimo Viável - Nível 1)

1. ✅ Feature engineering básico (temporal, aggregations)
2. ✅ Treinar XGBoost simples
3. ✅ Pipeline completo de treino → predict → output
4. ✅ Submeter Nível 1

### Fase 2 (Melhorias - Níveis 2-3)

1. ✅ Adicionar LightGBM e CatBoost ao ensemble
2. ✅ Feature engineering avançado (network, geo)
3. ✅ Otimização de threshold
4. ✅ Agentes especializados funcionais

### Fase 3 (Refinamento - Níveis 4-5)

1. ✅ Transfer learning entre níveis
2. ✅ Drift detection
3. ✅ Calibração adaptativa
4. ✅ Otimização de custos

---

## 📚 Recursos Úteis

- **Langfuse Docs:** https://langfuse.com/docs
- **LangChain Docs:** https://python.langchain.com/docs/
- **XGBoost Docs:** https://xgboost.readthedocs.io/
- **Scikit-learn Imbalanced:** https://imbalanced-learn.org/

---

## 🆘 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'xxx'"

```bash
pip install xxx
# ou
pip install -r requirements.txt
```

### Erro: "Langfuse connection failed"

- Verificar credenciais no .env
- Testar conexão internet
- Verificar LANGFUSE_HOST correto

### Erro: "Out of memory"

- Reduzir batch size
- Processar dados em chunks
- Usar menos modelos no ensemble

---

## 💪 Você Está Pronto!

O setup está completo. Agora é:

1. ✅ Instalar dependências
2. ✅ Validar com test_setup.py
3. ✅ Baixar dados do Nível 1
4. 🚀 Começar a implementação

**Boa sorte no desafio! 🎯**
