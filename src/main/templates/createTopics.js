var frontImages = [];
var backImage;
var x = ""
var frontstr = []

function preload() {
  // fig1 = "{% static 'img/0.png' %}"
  // print(fig1)
  // frontImages['0'] = loadImage("{% static 'img/0.png' %}");
  frontImages['0'] = loadImage("{% static 'img/0.png' %}");
  // frontImages['1'] = loadImage("img/1.png");
  // frontImages['2'] = loadImage("img/2.png");
  // frontImages['3'] = loadImage("img/3.png");
  // frontImages['4'] = loadImage("img/4.png");
  // frontImages['5'] = loadImage("img/5.png");
  backImage = loadImage("{% static 'img/baskside_min.png' %}");
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  var cardTypes = ['0', '1', '2', '3', '4', '5'];
  var card = createSprite(windowWidth / 2, windowHeight / 2 - 200);
  card.addImage('back', backImage);
  card.onMousePressed = function() {
    console.log(floor(random(frontstr.length)))
    x = frontstr[floor(random(frontstr.length))];
    text(x, windowWidth / 2, windowHeight / 2 + 200);
    // var card2 = createSprite(windowWidth/2, windowHeight/2+100);
    // card2.addImage('front', frontImages[cardTypes[floor(random(6))]]);
    // card2.changeImage('front');
    // drawSprites();
  }
}

function AddStringToTextarea() {
  var UserString = document.getElementById('sampleUserInput').value;
  // var user_id = "{{ user_id }}"
  // var partner_id = "{{ partner_id }}"
  // const url = 'http://127.0.0.1:8000/' + user_id + "/" + partner_id + "/" + "topic";

  // fetch(url).then(function(response) {
  //   console(response)
  // }).then(function(text) {
  //   console.log(text);
  // });

  var TargetList = document.getElementById('sampleInputedList');
  frontstr.push(UserString);
  console.log(frontstr.length);
}

function draw() {
  background(0, 0, 80);
  imageMode(CENTER);
  textSize(30);
  text(x, windowWidth / 2, windowHeight / 2 + 200);
  drawSprites();
}
