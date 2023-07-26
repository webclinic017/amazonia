# amazonia

Projeto sobre uma aplicação baseada na tecnologia eBPF.

@hudsoncoutinhoo




Apos o 'git clone'.

Construa os containers Docker, navegando até o diretório do projeto

$ cd nomedoprojeto

Construa usando o comando abaixo:

$ docker-compose up --build


*** Apos isso a aplicação deverá estar operacional em poucos minutos, vamos validar se esta tudo OK.

- Pimeiro acesse o frontend, digitando `http://localhost` ele estará acessível na porta 80 do host.

- Segundo passo é o backend, ele estará acessível em `http://localhost:5000/metrics`, e a coleta de métricas eBPF será executada em segundo plano, interagindo com o kernel.


Ponto de atenção:
Para executar eBPF no espaço do kernel dentro de um container Docker, 
você precisa ter privilégios de sistema (`--privileged`) ou habilitar recursos específicos do eBPF, como o modo de rede "host". 
