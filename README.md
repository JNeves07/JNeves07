<div align="center">

![Banner](https://capsule-render.vercel.app/api?type=waving&color=0:0A1F5C,50:2A4FC4,100:4169E1&height=240&section=header&text=João%20Marcelo&fontSize=60&fontColor=ffffff&fontAlignY=38&desc=Back-End%20Developer%20%7C%20Engenharia%20de%20Software%20%7C%20PHP%20%C2%B7%20Laravel%20%C2%B7%20Docker&descSize=17&descAlignY=60&animation=fadeIn)

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&pause=1200&color=5B7FEE&center=true&vCenter=true&width=620&lines=Back-End+com+PHP+%26+Laravel;Docker+%7C+APIs+%7C+Banco+de+Dados;Buscando+est%C3%A1gio+em+desenvolvimento+de+sistemas)](https://git.io/typing-svg)

[![PORTFÓLIO](https://img.shields.io/badge/PORTFÓLIO-4169E1?style=for-the-badge&logo=githubpages&logoColor=white)](https://jneves07.github.io)
[![LINKEDIN](https://img.shields.io/badge/LINKEDIN-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/joao-marcele-a30407336/)
[![EMAIL](https://img.shields.io/badge/EMAIL-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:marcelejoao7@gmail.com)
[![WHATSAPP](https://img.shields.io/badge/WHATSAPP-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/5599981897798)

</div>

---

## 👋 Sobre mim

<table>
<tr>
<td width="62%">

```js
const joao = {
  role: "Engenheiro de Software",
  focus: "Desenvolvedor Back-End",
  location: "Caxias, MA - Brasil 🇧🇷",

  working: {
    at: "Fábrica de Software - UniFacema",
    on: ["Sistemas institucionais",
         "Controle e análise de dados"],
  },

  studying: [
    "Engenharia de Software (7º período)",
    "Análise e Desenv. de Sistemas (4º)",
  ],

  learning: ["TypeScript", "Python p/ dados", "IoT"],

  languages: ["PT 🇧🇷", "EN B1", "ES B1", "Libras"],

  lookingFor: "Estágio em desenvolvimento",
};
```

</td>
<td align="center" width="38%">

[![Streak](https://streak-stats.demolab.com/?user=JNeves07&theme=tokyonight&hide_border=true&background=0D1117)](https://github.com/JNeves07)

</td>
</tr>
</table>

> *"Qualquer tolo escreve código que um computador entende. Bons programadores escrevem código que humanos entendem."* — **Martin Fowler**

> Antes de programar, fui **redator e professor**. Por isso gosto de código claro e de explicar soluções técnicas de um jeito que todo mundo entende.

---

## 🛠️ Tech Stack

<div align="center">

![Stack](https://skillicons.dev/icons?i=php,laravel,py,ts,js,dotnet,html,css,react,bootstrap,tailwind,docker,linux,nginx,mysql,postgres,git,github,vscode,postman,figma,ps,ai,bash&perline=12&theme=dark)

![APIs](https://img.shields.io/badge/APIs_REST-4169E1?style=flat-square)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![Kanban](https://img.shields.io/badge/Kanban-0052CC?style=flat-square&logo=trello&logoColor=white)
![IoT](https://img.shields.io/badge/IoT-00979D?style=flat-square&logo=arduino&logoColor=white)
![Redes](https://img.shields.io/badge/Redes_%26_Servidores-2A4FC4?style=flat-square)

</div>

---

## 📂 Projetos em destaque

| Projeto | Descrição | Tecnologias |
|---|---|---|
| **[Sistema-Academico](https://github.com/JNeves07/Sistema-Academico)** | Sistema para organizar e controlar dados acadêmicos. | `PHP` `Laravel` `MySQL` |
| **[pokedex](https://github.com/JNeves07/pokedex)** | Aplicação que lista e exibe informações de Pokémon. | `JavaScript` `APIs REST` |
| **[Programa-o-em-Banco-de-dados](https://github.com/JNeves07/Programa-o-em-Banco-de-dados)** | Exercícios de modelagem e consultas SQL. | `SQL` `MySQL` |

Veja todos os repositórios em [github.com/JNeves07](https://github.com/JNeves07?tab=repositories).

---

## 📊 GitHub Analytics

<div align="center">

<img src="./profile-summary-card-output/tokyonight/0-profile-details.svg" width="100%" alt="Perfil" />

<img src="./profile-summary-card-output/tokyonight/1-repos-per-language.svg" width="49%" alt="Linguagens por repositório" />
<img src="./profile-summary-card-output/tokyonight/4-productive-time.svg" width="49%" alt="Horário de commits" />

<img src="./profile-summary-card-output/tokyonight/3-stats.svg" width="49%" alt="Estatísticas" />
<img src="./profile-summary-card-output/tokyonight/2-most-commit-language.svg" width="49%" alt="Linguagens por commit" />

</div>

---

# 📘 Documentação do repositório

## Descrição

Este é o repositório de perfil do GitHub de **João Marcelo Neves de Lima**. Além da apresentação pública acima, ele concentra uma pequena ferramenta em **Python 3.15** para validar e resumir, localmente, as informações do perfil: tecnologias, estatísticas, projetos e os cartões SVG gerados pela GitHub Action de perfil.

Tudo funciona com a **biblioteca padrão do Python**: não é necessário instalar dependências com `pip`.

## Tecnologias

- **Python 3.15** (compatível com 3.13) — validação, resumo e testes com `unittest`.
- **GitHub Actions** — testes contínuos e geração diária dos cartões de perfil.
- **GitHub Profile Summary Cards** — action que produz os SVGs em `profile-summary-card-output/`.
- **JSON** — fonte única e simples de verdade em `profile-config.json`, sem PyYAML.
- **GitHub Pages** — portfólio publicado em [jneves07.github.io](https://jneves07.github.io).

## Arquitetura

```text
profile-config.json                 Dados do perfil (nome, stack, stats, projetos, cards)
        │
        ▼
tools/profile_summary.py            Carrega → valida → normaliza → resume
        │                              │
        │                              └── Verifica os SVGs do tema em
        │                                  profile-summary-card-output/<theme>/
        ▼
tests/test_profile_summary.py       unittest: validação, resumo e JSON inválido
        │
        ▼
.github/workflows/ci.yml             Python 3.13 e 3.15 no GitHub Actions
```

O fluxo é intencionalmente pequeno: `load_config()` lê o JSON com mensagens amigáveis, `validate_config()` devolve uma lista de problemas, `build_summary()` normaliza os dados e `format_summary()` prepara a saída para o terminal. A flag `--json` expõe o mesmo resumo de forma estruturada.

> Os SVGs em `profile-summary-card-output/` são gerados por `.github/workflows/profile-summary-cards.yml`. Eles são preservados e não devem ser editados manualmente.

## Como usar

Execute os comandos na raiz do repositório:

```bash
# Valida a configuração e verifica se os cartões do tema existem
python tools/profile_summary.py --validate

# Mostra o resumo legível de tecnologias e estatísticas
python tools/profile_summary.py --summary

# Valida e resume ao mesmo tempo (comando padrão, sem flags)
python tools/profile_summary.py

# Resumo estruturado para outras ferramentas
python tools/profile_summary.py --summary --json

# Usa outro arquivo e ignora a checagem dos SVGs
python tools/profile_summary.py --config outro-config.json --no-card-check
```

Para ajustar o perfil, edite `profile-config.json`. Campos obrigatórios: `username`, `name`, `role`, `technologies` e `stats`. Opcionais: `location`, `profile_url`, `portfolio_url`, `theme`, `featured_projects` e `cards`.

## Como testar

```bash
python -m unittest discover -s tests -v
```

A suíte cobre configuração válida, campos ausentes ou inválidos, cartões faltantes, resumo, saída em JSON, JSON corrompido e códigos de saída da CLI.

## CI

`.github/workflows/ci.yml` roda em *push* na branch `main`, em *pull requests* e manualmente. A matriz executa os testes e os comandos de validação/resumo no **Python 3.13 e 3.15**. O workflow de cartões continua separado, com agendamento diário às 03:00 (UTC-3) e execução manual.

Nenhum segredo é armazenado no repositório: o `GITHUB_TOKEN` usado pelo workflow de cartões é fornecido automaticamente pelo GitHub Actions.

## Estrutura

```text
.
├── .github/
│   └── workflows/
│       ├── ci.yml                      # Testes e validação (3.13 e 3.15)
│       └── profile-summary-cards.yml   # Geração dos SVGs (preservada)
├── profile-summary-card-output/        # SVGs de todos os temas gerados
├── profile-config.json                 # Configuração local do perfil
├── tools/
│   └── profile_summary.py              # CLI de validação e resumo
├── tests/
│   └── test_profile_summary.py         # Testes unittest
└── README.md                           # Perfil + documentação
```

<div align="center">

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:4169E1,50:2A4FC4,100:0A1F5C&height=100&section=footer)

</div>
