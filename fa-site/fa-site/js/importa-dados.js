
$.ajax(
  {
    url: 'https://s3.amazonaws.com/image-recognition-alura-website/data.json',
    dataType: 'json',
    crossDomain: true,
    success: function (data) {
      console.log(data);
      montaTabela(data);
    }
  })


function montaTabela(data) {


  for (var data of data) {
    var trTabela = document.createElement("tr");

    var tdInfoFoto = document.createElement("td");
    var tdInfoNome = document.createElement("td");
    var tdInfoFaceMatch = document.createElement("td");


    tdInfoNome.textContent = data.name;
    tdInfoFaceMatch.textContent = data.similarity;
    tdInfoFoto = document.createElement("img");
    tdInfoFoto.height = 100;
    tdInfoFoto.width = 68;
    tdInfoFoto.src = 'https://image-recognition-alura.s3.amazonaws.com/' + data.name + '.jpg';

    trTabela.appendChild(tdInfoFoto);
    trTabela.appendChild(tdInfoNome);
    trTabela.appendChild(tdInfoFaceMatch);

    var tabela = document.querySelector("#tabela-site");

    tabela.appendChild(trTabela);
  }
}
