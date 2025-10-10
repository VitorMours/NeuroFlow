- [x] Terminar servico de autenticacao do signin - Finished in 16-06-2025
    - [x] Terminar o servico de Signin, com hash de senhas, 
    - [ ] Logar o usuario automaticamente dentro da sessao depois de fazer o login ou sign de maneira coreta dentro da paltaforma
    - [x] Fazer uma verififcacao do banco de dados antes de salvar o usuario, de forma que facilite a forma de verfiicar se o usuario ja existe, ou se tem algum problema dele ser cadastrado
    
- [ ] Crair scrpits javascript para receber os dados provenientes do flask 
- [x] Estudar a diferenca entre PWA e SPA
- [ ] Estudarsobre a possibilidade de colocar essa aplicação como um PWA


# 05/07/2025

- [ ] Create the security for the pagesto user to be logged to access 



# 07/07/2025
Foi feito todo o esquema de criação, e de desenvolvimento das tasks que estão linkadas por meio de chave estrangeira com usuário, fazendo com que seja impossível criar uma task, sem que tenha um usuário cadastrado dentro da base de dados que 
esteja em vias de fato conectado com essa task.
Com isso, agora torna-se apenas necessário fazer o desenvolvimento do macro necessário para que sejam mostradas as tasks 
dentro da interface para o usuário, de forma que são aplicados filtros dentro dessa interface, em que dividimos as tasks
em todas, as tasks ativas, e as tasks que já foram concluída. Com isso, temos a necessidade de codificar ainda o desenvolvimento das possibilidades de edição e de deleção de alguma task por parte do usuário


# 08/07/2025
Atualmente a funcionalidade de criar e mostrar as tasks esta correta, entretanto precisa-se fazer com que ao criar uma nova task, ela seja automaticamente enviada
e mostrada dentro da interface, para que possamos ter mais interatividade e fique mais facil para o usuario. Estou pensando em usar o localStorage do javascript apra quando tiver uma task dentro da interface criada que ainda nao foi enviada para o banco de dados, ela ficar salva e mostrada, de forma que fique mais facil de trabalhar com ela enquanto nao consigo dar auto-browser-referesh dentro da itnerface por mei odo backend

# 12/07/2025
Percebi que preciso modificar dentro da parte de todo o template, todas as tasks devem ser gerenciadas dentro da pagina, e nao dentro do macro, de forma que eu defino anteriormente a injecao das tasks, oque deve ser enviado para ser mostrado ou nao, por meio de parametros dentro do proprio template


# 14/07/2025
Dentro do caso da funcionalidade das tasks, posso tentar criar um endpoint em que recebe esse comportamento de fazer o 
"toggle" entre a conclusao das tasks, e com base nele, modificar o comportamento naquele caso especifico, a cada clique.
Com isso das duas uma, ou eu posso fazer em batch, ou de forma unica:

> Quando digo em batch, significa que posso ficar recebendo todas as tasks que sao modificadas, e somente apos sair da rota 
a qual o mesmo se encontra presente, ou mudar de aba, da ativa para geral por exemplo, enviar as tasks, e antes de serem mostradas, fazer as modificacoes necessarias. Por outro lado, posso fazer essas modificacoes no mesmo momento em que elas sao 
acionadas, de forma a evitar possiveis mutacoes e duplicacoes de comportamento dentro da aplicacao. Preciso verificar isso.

# 16/07/2025
pelo visto dentro da parte de todo, vou ter que fazer toda a interacao sendo feita totalmente pelo javascript, sem um pingo de 
jinja sendo o foco do desenvolvimento. Com isso, vou ter que focar totalmente nas bases de desenvolvimento do javascript, e focar
na forma como vou manipular o DOM, de forma que quando eu precise atualizar as tasks, seja rapido e eficiente, pois toda vez
que eu trocar de aba, ou criar uma nova task tenho, salvar as modificacoes que foram feitas.



# 28/07/2025
- [x] Ainda precisa ser feito o script javascript para enviar a delecao de tasks





# 17/08/2025
- [ ] Modificar todos os arquivos que possuem base.html para base.jinja


# 18/08/2025
- [ ] Adicionar docker dentro da estrutura de forma que facilite o desenvolvimento em diferentes ambientes 


# 08/09/2025 
- [x] Fazer a landing page sem a parte de contanto
- [x] Fazer o rodape com o link de email e o link do linkedin
- [ ] Criar o sistema de temas com javascript dentro do projeto
- [ ] Fazer o sistema de anoteções e de tasks dentro do projeto 

# 29/09/2025
- [ ] Corrigir o sistema responsável por fazer o todo dentro do flask