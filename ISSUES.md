# Padrão de issue para criação sem formulário

Este arquivo é a fonte única da regra para quem cria issue sem o formulário do GitHub: por API, CLI, modelo de IA ou outra ferramenta.

Quando possível, o formulário do GitHub é o caminho preferido. Ele aplica o título, as labels e o corpo no formato abaixo. Use este padrão quando a issue for criada fora do formulário.

Os quatro tipos seguem a ordem do seletor. O GitHub lista os arquivos de `.github/ISSUE_TEMPLATE/` em ordem alfanumérica: `bug.yml`, `feature.yml`, `question.yml`, `task.yml`. No `config.yml`, `blank_issues_enabled` está `false`: o caminho da interface é um desses formulários.

## Como escolher o repositório

O atalho do seletor se chama "Qual repositório usar". Veja em qual repositório fica cada sistema antes de abrir a issue.

https://github.com/wisermeter/workflows/blob/main/README.md#como-abrir-uma-issue

## Chamado de cliente final

Chamado de cliente final não vira issue. Ele vai para o GLPI: https://desk.seuconsumo.com.br/

Cliente final e parceiros abrem chamado pelo GLPI, não pelo GitHub.

## O que não entra na issue

Nunca coloque dado pessoal (LGPD): CPF, e-mail, telefone ou endereço de moradores ou de clientes finais. Nunca coloque credencial: senha, token ou chave.

No identificador e no anexo, o formulário traz este aviso:

Só o código ou número. Não coloque nome, CPF, e-mail, telefone ou endereço.

Antes de anexar prints ou arquivos, recorte ou borre nome, CPF, e-mail, telefone, endereço e dados de terceiros. Depois de publicado, o anexo continua acessível mesmo que você apague.

O campo Anexos, em qualquer tipo, segue esse aviso. Sem arquivo, a seção fica `_No response_`.

## Formato do corpo

Cada seção vira um cabeçalho `### Título do campo` seguido do conteúdo. O título do cabeçalho é o `label` do campo, idêntico, com os mesmos acentos e a mesma pontuação. É o formato que o GitHub gera a partir do formulário.

Há uma linha em branco entre o cabeçalho e o conteúdo, e uma linha em branco entre as seções. O corpo inclui todas as seções do tipo, na mesma ordem, inclusive as opcionais.

Seção opcional sem conteúdo leva `_No response_`. Esse é o formato aceito: é o que o GitHub gera para campo de texto (`input`, `textarea`) e para anexo vazio. Dropdown opcional sem escolha leva `None`.

Em dropdown, o conteúdo é o texto exato de uma das opções. Seção obrigatória leva conteúdo.

O título da issue é outro campo: começa com o prefixo do tipo, espaço final incluído. O restante é uma frase curta, sem dado pessoal e sem credencial.

As labels do tipo vão no pedido de criação. Pelo formulário, o GitHub aplica o campo `labels`. Pela API, CLI ou outra ferramenta, quem abre a issue envia as mesmas labels.

Chamado GLPI de origem, quando houver número: Preencha se veio de um chamado do GLPI. Ex.: 2814. Sem chamado, a seção fica `_No response_`.

Modelo:

```markdown
### Título do campo

conteúdo da seção
```

## Algo não funciona

Formulário: [`.github/ISSUE_TEMPLATE/bug.yml`](.github/ISSUE_TEMPLATE/bug.yml). No seletor: O sistema deu erro ou fez diferente do esperado.

**Título padrão:** `[Bug] ` (o prefixo inclui o espaço final)

**Labels:** `type: bug`, `status: needs-triage`

Aplique estas labels na issue.

Formato do corpo: cada seção da lista entra na issue, na mesma ordem, como um cabeçalho `### Título do campo` seguido do conteúdo. O título do cabeçalho é o texto da seção, idêntico. É o formato que o GitHub gera a partir do formulário. Seção opcional sem conteúdo leva `_No response_` (formato aceito). Dropdown opcional sem escolha leva `None`. O campo Anexos segue o aviso da seção «O que não entra na issue».

1. **O que o cliente estava fazendo?** — obrigatória
2. **O que ele esperava que acontecesse?** — obrigatória
3. **O que aconteceu de fato?** — obrigatória
4. **Quando aconteceu?** — obrigatória
   Data e hora aproximadas. Se o cliente não souber, escreva 'não sei'.
5. **Acontece sempre ou foi uma vez?** — opcional. Opções: `Sempre`, `Às vezes`, `Uma vez`, `Não sei`
6. **Onde: celular, computador ou tablet?** — opcional. Opções: `Celular`, `Computador`, `Tablet`, `Não sei`
7. **Impacto** — obrigatória. Opções: `Não consigo trabalhar`, `Consigo, mas com dificuldade`, `Pequeno incômodo`
8. **Chamado GLPI de origem** — opcional
9. **Identificador do cliente ou do registro afetado (código do condomínio, da unidade, do medidor, da fatura, da embarcação ou do equipamento)** — opcional
10. **Anexos** — opcional

Título da issue: `[Bug] Relatório do condomínio COND-1042 abre em branco`

Exemplo de corpo completo, com dados fictícios:

```markdown
### O que o cliente estava fazendo?

Pediu o relatório de consumo de março de 2026 do condomínio COND-1042.

### O que ele esperava que acontecesse?

A tela abriria com o total do condomínio no mês.

### O que aconteceu de fato?

A tela ficou em branco e mostrou a mensagem "erro ao carregar".

### Quando aconteceu?

04/08/2026, por volta de 14h.

### Acontece sempre ou foi uma vez?

Sempre

### Onde: celular, computador ou tablet?

None

### Impacto

Não consigo trabalhar

### Chamado GLPI de origem

0000

### Identificador do cliente ou do registro afetado (código do condomínio, da unidade, do medidor, da fatura, da embarcação ou do equipamento)

COND-1042

### Anexos

_No response_
```

## Nova funcionalidade ou melhoria

Formulário: [`.github/ISSUE_TEMPLATE/feature.yml`](.github/ISSUE_TEMPLATE/feature.yml). No seletor: O cliente quer fazer algo que o sistema ainda não faz, ou fazer melhor o que já faz.

**Título padrão:** `[Feature] ` (o prefixo inclui o espaço final)

**Labels:** `type: feature`, `status: needs-refinement`

Aplique estas labels na issue.

Formato do corpo: cada seção da lista entra na issue, na mesma ordem, como um cabeçalho `### Título do campo` seguido do conteúdo. O título do cabeçalho é o texto da seção, idêntico. É o formato que o GitHub gera a partir do formulário. Seção opcional sem conteúdo leva `_No response_` (formato aceito). Dropdown opcional sem escolha leva `None`. O campo Anexos segue o aviso da seção «O que não entra na issue».

1. **O que o cliente quer resolver?** — obrigatória
2. **O que ele quer conseguir fazer depois?** — opcional
3. **Regras que você já sabe (limites, condições, exceções)** — opcional
4. **Como o cliente vai saber que ficou pronto?** — opcional
5. **Prioridade** — opcional. Opções: `Baixa`, `Média`, `Alta`
   No formulário, a opção pré-selecionada é Média. Fora do formulário, escreva a opção escolhida.
6. **Chamado GLPI de origem** — opcional
7. **Identificador do cliente ou do registro afetado (código do condomínio, da unidade, do medidor, da fatura, da embarcação ou do equipamento)** — opcional
8. **Anexos** — opcional

Título da issue: `[Feature] Exportar o consumo do mês em planilha`

Exemplo de corpo completo, com dados fictícios:

```markdown
### O que o cliente quer resolver?

O condomínio COND-2201 quer baixar o consumo do mês em planilha.

### O que ele quer conseguir fazer depois?

Gerar um arquivo com uma linha por unidade e o consumo daquele mês.

### Regras que você já sabe (limites, condições, exceções)

_No response_

### Como o cliente vai saber que ficou pronto?

A soma das linhas fecha com o total do condomínio no mês.

### Prioridade

Média

### Chamado GLPI de origem

_No response_

### Identificador do cliente ou do registro afetado (código do condomínio, da unidade, do medidor, da fatura, da embarcação ou do equipamento)

COND-2201

### Anexos

_No response_
```

## Dúvida de uso

Formulário: [`.github/ISSUE_TEMPLATE/question.yml`](.github/ISSUE_TEMPLATE/question.yml). No seletor: O cliente não sabe como fazer algo no sistema.

**Título padrão:** `[Question] ` (o prefixo inclui o espaço final)

**Labels:** `type: question`

Aplique estas labels na issue.

Formato do corpo: cada seção da lista entra na issue, na mesma ordem, como um cabeçalho `### Título do campo` seguido do conteúdo. O título do cabeçalho é o texto da seção, idêntico. É o formato que o GitHub gera a partir do formulário. Seção opcional sem conteúdo leva `_No response_` (formato aceito). Dropdown opcional sem escolha leva `None`. O campo Anexos segue o aviso da seção «O que não entra na issue».

1. **Qual é a dúvida do cliente?** — obrigatória
2. **Chamado GLPI de origem** — opcional
3. **Identificador do cliente ou do registro afetado (código do condomínio, da unidade, do medidor, da fatura, da embarcação ou do equipamento)** — opcional
4. **Anexos** — opcional

Título da issue: `[Question] Como achar a fatura FAT-2026-0312 pelo medidor`

Exemplo de corpo completo, com dados fictícios:

```markdown
### Qual é a dúvida do cliente?

Como localizar a fatura FAT-2026-0312 a partir do código do medidor MED-7781.

### Chamado GLPI de origem

0000

### Identificador do cliente ou do registro afetado (código do condomínio, da unidade, do medidor, da fatura, da embarcação ou do equipamento)

MED-7781

### Anexos

_No response_
```

## Tarefa (carga de dados, configuração)

Formulário: [`.github/ISSUE_TEMPLATE/task.yml`](.github/ISSUE_TEMPLATE/task.yml). No seletor: Algo a ser feito uma vez, sem regra nova. Ex.: importar uma planilha.

**Título padrão:** `[Task] ` (o prefixo inclui o espaço final)

**Labels:** `type: task`

Aplique estas labels na issue.

Formato do corpo: cada seção da lista entra na issue, na mesma ordem, como um cabeçalho `### Título do campo` seguido do conteúdo. O título do cabeçalho é o texto da seção, idêntico. É o formato que o GitHub gera a partir do formulário. Seção opcional sem conteúdo leva `_No response_` (formato aceito). Dropdown opcional sem escolha leva `None`. O campo Anexos segue o aviso da seção «O que não entra na issue».

1. **O que precisa ser feito?** — obrigatória
2. **Prazo desejado** — opcional
3. **O que o cliente espera ver no final?** — obrigatória
4. **Chamado GLPI de origem** — opcional
5. **Identificador do cliente ou do registro afetado (código do condomínio, da unidade, do medidor, da fatura, da embarcação ou do equipamento)** — opcional
6. **Anexos** — opcional

Título da issue: `[Task] Importar equipamentos do condomínio COND-2201`

Exemplo de corpo completo, com dados fictícios:

```markdown
### O que precisa ser feito?

Importar a planilha de equipamentos do condomínio COND-2201, com as colunas código e leitura inicial.

### Prazo desejado

_No response_

### O que o cliente espera ver no final?

Os equipamentos EQ-440 e EQ-441 aparecem na lista do condomínio com a leitura inicial da planilha.

### Chamado GLPI de origem

_No response_

### Identificador do cliente ou do registro afetado (código do condomínio, da unidade, do medidor, da fatura, da embarcação ou do equipamento)

EQ-440

### Anexos

_No response_
```

## Manutenção

Se um formulário em `.github/ISSUE_TEMPLATE/` mudar (`bug.yml`, `feature.yml`, `question.yml`, `task.yml`), este arquivo muda no mesmo pull request. O mesmo vale para `config.yml`, de onde saem o link do GLPI e o link de escolha de repositório.

Título padrão, labels, títulos de seção, obrigatoriedade e opções de dropdown daqui acompanham o YAML. O workflow `.github/workflows/issue-forms.yml` roda `scripts/check_issues_md.py`, que confere título de seção, label, obrigatoriedade e opções de dropdown com o YAML.
