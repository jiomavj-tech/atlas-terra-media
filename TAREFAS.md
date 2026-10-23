# Tarefas — em ordem de prioridade

Situação atual: v7.9 (23/10/2026). Tarefas 1 a 4 resolvidas; pendentes: 5 e 6. Use `python tools/teste_fumaca.py` para reproduzir os erros.

---

## ✅ Tarefa 1 — Grafo principal não abre (ALTA) — RESOLVIDA na v7.8

**Problema:** ao escolher **Menu → Grafo principal**, a tela não troca. O desenho do grafo trava antes de terminar. Os botões das seções **Obras** e **Genealogias clássicas** que levam ao grafo também disparam o erro.

**Erro:** `TypeError: Cannot read properties of undefined (reading 'x')` dentro de `draw()`, no trecho
`E.forEach(e=>{...const a=byId[e.a],b=byId[e.b];el('line',{x1:a.x,...`
A chamada vem de `window.atlasMainGraphStart` → `refresh()` → `draw()`.

**Causa provável:** alguma relação em `E` aponta para um id que não está em `byId`, ou para um nó que não recebeu posição (`x`/`y`). Isso acontece, por exemplo, quando um nó é acrescentado a `N` depois de `byId` ser montado.

**Pronto quando:**
- O grafo abre no celular (400 px) e no computador.
- Nenhuma relação inválida derruba o desenho: ela é ignorada e listada com `console.warn`.
- O teste de fumaça não mostra mais erros em `[grafo]`, `[obras]` e `[genealogy]`.

---

## ✅ Tarefa 2 — Pontos sem posição na Cronologia (ALTA) — RESOLVIDA na v7.8

**Problema:** na seção **Cronologia**, alguns eventos são desenhados com coordenada `undefined`/`NaN` e não aparecem no gráfico.

**Erro:** `<circle> attribute cx: Expected length, "undefined"` (e o mesmo para `cy`, `x` e `y`).

**Pronto quando:**
- Os eventos sem ano ou sem posição calculável não são desenhados, e aparecem num aviso discreto "sem data definida", ou recebem uma posição válida.
- O teste de fumaça não mostra mais erros em `[cronologia]`.

---

## ✅ Tarefa 3 — Versões desencontradas (MÉDIA) — RESOLVIDA na v7.8

**Problema:** o `<title>` diz v7.7, o cabeçalho dizia "Versão 6.3" e os comentários do código citam v7.6. Isso confunde na hora de saber qual arquivo é o mais novo.

**Pronto quando:**
- Existe uma constante única, por exemplo `window.ATLAS_VERSAO = '7.8'`, e o título e o cabeçalho leem dela.
- O `CHANGELOG.md` registra as versões a partir da 7.7.

---

## ✅ Tarefa 4 — Bloco largo demais na Genealogia completa (BAIXA) — RESOLVIDA na v7.8

**Problema:** na seção **Genealogias completas** (`#atlas-genealogia`), um elemento passa da largura da tela do celular e obriga a rolar para o lado.

**Pronto quando:** em 360 px e em 400 px de largura não existe rolagem horizontal na página. A árvore pode rolar dentro da própria caixa, mas a página não.

---

## Tarefa 5 — Auditoria de conexões: 158 de 190 com pendência (MÉDIA, em lotes)

**Problema:** a auditoria (`window.atlasRelationsAuditV76()`) lista 190 personagens, e 158 deles têm conexões que não batem com outras fichas (`unresolved_connection_labels`).

**Como fazer:** em lotes de 20 personagens, um lote por PR. Ligue cada rótulo pendente a uma ficha existente (`resolved_connection_keys`). Quando não houver ficha correspondente, deixe o rótulo como pendente. **Não invente relações.** Use só o que está em Tolkien ou na obra citada na ficha.

**Pronto quando:** o número de pendências cai, e cada PR lista quais ligações foram feitas e a fonte de cada uma.

---

## Tarefa 6 — Resumos da Wikipédia em inglês e só com internet (BAIXA)

**Problema:** a seção Pessoas busca resumos em `en.wikipedia.org`. Sem internet, a busca falha, e com internet o texto vem em inglês.

**Pronto quando:** a busca tenta primeiro `pt.wikipedia.org` e só usa a versão em inglês se não achar. Sem internet, aparece uma mensagem amigável e nenhum erro.
