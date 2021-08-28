# projeto-ope
Este repositório é dedicado ao desenvolvimento do projeto requerido na disciplina de OPE II da Faculdade Impacta de Tecnologia.


<h1> Anotações importantes sobre o projeto e sobre como ele está sendo desenvolvido. </h1>

<h2>Abaixo contém a explicação sobre como o projeto está sendo estruturado.</h2>

<p> Primeiro criamos um pacote Python chamado "app" que conterá todo o código do nosso sistema.
Dentro deste pacote os arquivos são separados de acordo com "interesses", seguem exemplos abaixo: </p>

<h3> app - (__init__.py) </h3>
<p> Este arquivo é o "Core" do sistema, onde o Flask é inicializado e os pacotes e extensões são instanciadas para podemos usá-las </p>

<h3> Rotas - (routes.py) </h3>
Temos o arquivo de routes.py que obviamente contém as rotas e seus respectivos métodos, algo que seria como um "Controller" fazendo uma analogia ao MVC. Os métodos normalmente possuirão uma lógica associada ao template (View) que irá retornar. </p> </br>

<h3> Views/Telas - (templates) </h3>
<p> Todos os arquivos HTML/Jinja2 deverá estar nesta pasta, pois é desta forma que o Flask pode idetificá-los, o "Template Engine" do Flask é o Jinja2 que nos possibilita escrever lógica para interagir com o código HTML, como loops, condicionais, imprimir variáveis e etc. </p>


<h3> Formulários (forms.py) </h3>
<p> Neste projeto usaremos a extensão FlaskWTF, que é pertence ao pacote WTForms que também usaremos para obter mais recursos relacionados a formulários e suas validações. O uso deste pacote está restrito ao arquivo forms.py </p>

-----------------------------------------------------------------------------------------------------------
<h2> Arquivos fora do pacote do sistema </h2>

<h3>.flaskenv</h3>
<p>Este arquivo está relacionado a extensão python-dotenv, ele possibilita que configuremos variáveis de ambiente no momento em que o Flask é inicializado, permitindo a execução da aplicação com o comando "flask run". Pra isso funcionar foi necessário declara a variável FLASK_APP=app-instance, que aponta o app-instance como instancia do sistema. </p>

<h3> app-instance.py (Instância do pacote/projeto )</h3>
<p> O app-instance.py é a instância do nosso pacote "app", é como se fosse uma espécie de executável, ele importa o app e quando rodamos o comando "flask run" que está associado a ele por meio da variável de ambiente FLASK_APP a aplicação é executada. </p>

<h3>Configurações da aplicação - (config.py)</h3>
<p>Este módulo é guarda na classe Config algumas configurações importantes para o uso de algumas extensões, como a SECRET_KEY por exemplo que é necessária para o funcionamento da extensão FlaskWTF além de outras coisas, no caso da FlaskWTF, ela serve para servir como base de app_key para o uso do CSFR Token nos formulários. </p>