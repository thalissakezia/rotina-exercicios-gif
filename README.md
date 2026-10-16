# Rotina semanal de exercícios animados

Projeto de treino com foco em glúteos, braços, core e postura, priorizando exercícios no tapete.

## O que será produzido
Sete GIFs por dia (um para cada dia da semana), GIFs individuais e painel HTML com animações em grade.
Cada exercício traz nome, explicação, músculos trabalhados, séries/repetições ou duração.

## Organização
- data/exercicios.json: catálogo com referências exatas aos exercícios
- data/dias: um JSON separado para cada dia
- scripts/build.py: produz cartões e animações sem API paga
- output/daily: GIFs completos por dia (gerados pelo GitHub Actions)
- output/gifs: GIFs individuais
- output/semana.html: painel semanal

## Fidelidade e limitações
Os movimentos com referência usam 3 poses ilustradas do Workout Guide, não geração livre por IA.
Os 3 quadros permitem demonstrar posições, mas não comprovam biomecânica de toda a trajetória.
A elevação interna de perna permanece marcada como pendente; não será disfarçada como elevação externa.
O agachamento sumô foi provisoriamente substituído por agachamento sem carga; a ênfase em adutores não é igual.
Exercícios não reduzem gordura localizada de braços ou barriga. Ajuste a intensidade à condição individual;
no período após a gravidez, atenção a sintomas pélvicos, dor ou desconforto e obtenha orientação de profissional.

## Fontes e licenças
Desenhos: Bryl Lim / Workout Guide e Everkinetic, sob CC BY-SA 4.0.
Adaptações seguem os termos de atribuição e compartilhamento da mesma licença.
Consulte docs/REFERENCIAS.md.

## Como gerar
Python 3.11; pip install -r requirements.txt; python scripts/validate.py; python scripts/build.py
A automação GitHub Actions gera novamente em cada alteração da base.

## Abrir os arquivos animados

- [Segunda-feira](output/daily/segunda.gif)
- [Terça-feira](output/daily/terca.gif)
- [Quarta-feira](output/daily/quarta.gif)
- [Quinta-feira](output/daily/quinta.gif)
- [Sexta-feira](output/daily/sexta.gif)
- [Sábado](output/daily/sabado.gif)
- [Domingo](output/daily/domingo.gif)

- [GIFs individuais](output/gifs/)
- [Painel de toda a semana](output/semana.html)

O painel HTML precisa ser aberto com os GIFs na pasta ao lado. O pacote completo também aparece nos artefatos do GitHub Actions.
