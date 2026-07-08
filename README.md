# ☀️ Solaris 

**Marketplace de comparação de orçamentos de energia solar fotovoltaica**

Projeto acadêmico desenvolvido na disciplina de Projetos 1 — Gestão de Tecnologia da Informação (GTI), CESAR School · Equipe 5 · 2026.1

---

## 🎯 O problema

O consumidor brasileiro que quer instalar energia solar não consegue comparar orçamentos de forma objetiva. Cada instaladora entrega propostas em formatos próprios — PDFs por WhatsApp, planilhas, links de softwares internos — com informações em ordens diferentes, linguagem técnica inacessível e itens incluídos ou omitidos de maneira distinta em cada proposta.

O contexto agrava o problema: o Brasil ultrapassou **68 GW de capacidade solar instalada** (ANEEL, mar/2026), com mais de **26 mil empresas** no setor e ~450 novos integradores cadastrados por mês — 70% deles sem experiência prévia no mercado. Resultado: um mercado extremamente fragmentado, sem padrão de comunicação com o consumidor.

Validamos o problema em múltiplas frentes: relatos diretos de consumidores, reclamações registradas na ouvidoria da ANEEL e em Procons, análises de especialistas do setor e literatura acadêmica sobre transparência de preços em mercados solares — além de **pesquisa primária própria** com consumidores de Pernambuco.

## 💡 A solução

Um marketplace onde as empresas integradoras cadastram orçamentos em **campos padronizados** definidos pela plataforma, com custos discriminados (painéis, inversor, mão de obra, taxas). O consumidor visualiza uma **tabela comparativa lado a lado** e entende exatamente por que uma proposta é mais cara que outra.

Funcionalidades centrais:

- 📋 **Orçamento padronizado** — especificações técnicas, custos itemizados, garantias e checklist de escopo em campos comuns a todas as propostas
- ⚖️ **Comparador visual** — propostas alinhadas critério a critério, no estilo dos comparadores de eletrônicos
- 🔄 **Dois fluxos de ator** — jornada do consumidor (buscar, comparar, decidir) e jornada da integradora (cadastrar, gerenciar propostas), com mecanismo de conversão visitante → usuário logado

## 🔬 Como chegamos aqui

O projeto seguiu um processo completo de descoberta e definição:

1. **Pesquisa e validação do problema** — levantamento documental + pesquisa primária com consumidores (Google Forms, PE)
2. **Análise competitiva** — 9 plataformas nacionais e internacionais avaliadas sob 13 critérios derivados das dores identificadas
3. **Ideação estruturada** — sessão de BrainWrite 6-3-5 documentada no Miro, com 2 rodadas de votação entre 5 ideias finalistas
4. **Definição da solução** — fluxograma completo dos dois atores, definição de campos e funcionalidades ancorada nas dores mapeadas
5. **Desenvolvimento e iteração** — desenvolvimento de um CRUD em Python com leitura de dados txt
6. **Entregas avaliativas** — apresentações SR1 e SR2 + dossiê completo do projeto publicado no Google Sites

## 👥 Equipe 

| Integrante | Frente |
|---|---|
| **Laura Brafman** | Design e Desenvolvimento |
| **Renata Vasconcelos** | Pesquisa e marketing |
| **José Jorge Macedo** | Pesquisa e Desenvolvimento |
| **Isaac Faye** | Pesquisa |
