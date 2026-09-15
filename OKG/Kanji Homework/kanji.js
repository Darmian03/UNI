

// предварително зареждане на звуковите ефекти

var slideSound = new Audio( 'slide.wav' ),
	boomSound = new Audio( 'boom.wav' );
	
	
// рисувателното поле на цял екран

var renderer = new THREE.WebGLRenderer( {antialias: true} );
	renderer.setAnimationLoop( drawFrame );
	renderer.setSize( innerWidth, innerHeight );
	

// сцена и камера

var scene = new THREE.Scene();
	camera = new THREE.PerspectiveCamera( 30, innerWidth/innerHeight, 0.1, 1000 );


// четири светлини с различни цветове

var lights = [
		new THREE.PointLight( 'dodgerblue' ),
		new THREE.PointLight( 'hotpink' ),
		new THREE.PointLight( 'cyan' ),
		new THREE.PointLight( 'fuchsia' ),
	];
	scene.add( ...lights );


// земя

var ground = new THREE.Mesh(
		new THREE.PlaneGeometry( 5000, 5000 ),
		new THREE.MeshPhongMaterial( {color: 'goldenrod'} )
	);
	ground.position.y = -11;
	ground.rotation.x = -Math.PI/2;
	scene.add( ground );


// прозрачна рамка

var boxFrame = new THREE.Mesh(
		new THREE.BoxGeometry( 21, 21, 11 ),
		new THREE.MeshPhongMaterial( {color: 'white', shininess: 220, opacity: 0.45, transparent: true, side: THREE.DoubleSide} )
	);
	boxFrame.add( new THREE.BoxHelper(boxFrame,'white') );
	boxFrame.visible = false;
	scene.add( boxFrame );


// реакция при промяна на размера на прозореца

window.addEventListener( 'resize', (event) => {
    camera.aspect = innerWidth/innerHeight;
    camera.updateProjectionMatrix( );
    renderer.setSize( innerWidth, innerHeight );
});

	
// закачане на графичното поле и ослушване за някои събития

window.addEventListener( 'load', function() {
	document.body.appendChild( renderer.domElement );
	document.body.addEventListener( 'click', frameSlide );
	document.body.addEventListener( 'keypress', frameSlide );
	document.body.addEventListener( 'contextmenu', frameSlide );
});

function frameSlide( event )
{
	if( event.button==0 || event.keyCode==32 )
	{
		// стартира плъзгане в обратна посока
		if( time-slideTime < T )
			slideTime = time + T-(time-slideTime);
		else
			slideTime = time;
		
		slideDir = -slideDir;
		slideSound.play();
		boom = slideDir<0;
	}
	else
	{
		// показва се или се скрива рамката
		event.preventDefault();
		boxFrame.visible = !boxFrame.visible;
	}
}
	
		

// функция за анимиране на сцената

const T = 0.8;		// време за плъзгане

var slideDir = -1,	// посока на плъзгане
	time,			// текущо време
	slideTime,		// начало на плъзгането
	vib = 0,		// амплитуда на вибрация
	boom = false;	// дали трябва да се прави буууум
	
function drawFrame( t )
{
	// време от милисекунди в секунди
	time = t/1000;

	// плъзгане за T секунди само
	if( time-slideTime < T )
	{
		part1.position.x = 2 + 2*slideDir*Math.sin( ((time-slideTime)/T-0.5)*Math.PI );
		part2.position.x = -part1.position.x;
	}
	
	// буум при "затваряне" на йероглифа
	if( boom && time-slideTime > T-0.1 )
	{
		boom = false;
		boomSound.play();
		vib = 1;
	}
	
	// непрекъснато въртене на сцената
	scene.rotation.x = 0.1 * Math.sin( time+1 );
	scene.rotation.y = 0.5 * Math.sin( time+2 );
	scene.rotation.z = 0.1 * Math.cos( time+3 );

	// вибриране на камерата
	camera.position.set( 0, 3-Math.sin(50*time)*vib, 60 );
	camera.lookAt( new THREE.Vector3( 0, Math.sin(50*time)*vib, 0 ) );
	vib = vib*0.96;

	// движение на светлините
	for (var i=0; i<4; i++)
	{
		var angle = time+Math.PI/2*i;
		lights[i].position.set(
			     25*Math.cos( angle ),
			 5 + 10*Math.sin( 1.5*angle ),
			15 +  5*Math.cos( 2*angle )
		);
	}
	
	//рисуване на сцената
	renderer.render( scene, camera );
}		

	
// в двата обекта се слагат половините на йероглифа

var part1 = new THREE.Group( ),
	part2 = new THREE.Group( );
	
scene.add( part1, part2 );
