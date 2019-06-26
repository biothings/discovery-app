(function (cjs, an) {

var p; // shortcut to reference prototypes
var lib={};var ss={};var img={};
lib.ssMetadata = [
		{name:"logo_atlas_", frames: [[0,0,387,774],[389,0,274,547],[389,549,195,389]]}
];


// symbols:



(lib.CachedTexturedBitmap_152 = function() {
	this.initialize(ss["logo_atlas_"]);
	this.gotoAndStop(0);
}).prototype = p = new cjs.Sprite();



(lib.CachedTexturedBitmap_153 = function() {
	this.initialize(ss["logo_atlas_"]);
	this.gotoAndStop(1);
}).prototype = p = new cjs.Sprite();



(lib.CachedTexturedBitmap_154 = function() {
	this.initialize(ss["logo_atlas_"]);
	this.gotoAndStop(2);
}).prototype = p = new cjs.Sprite();



(lib.Tween3 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer_1
	this.instance = new lib.CachedTexturedBitmap_154();
	this.instance.parent = this;
	this.instance.setTransform(-48.65,-97.35,0.5,0.5);

	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-48.6,-97.3,97.5,194.5);


(lib.Tween2 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer_1
	this.instance = new lib.CachedTexturedBitmap_153();
	this.instance.parent = this;
	this.instance.setTransform(-68.4,-136.8,0.5,0.5);

	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-68.4,-136.8,137,273.5);


(lib.Tween1 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer_1
	this.instance = new lib.CachedTexturedBitmap_152();
	this.instance.parent = this;
	this.instance.setTransform(-96.8,-193.6,0.5,0.5);

	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-96.8,-193.6,193.5,387);


(lib.Scene_1_main = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// main
	this.instance = new lib.Tween3("synched",0);
	this.instance.parent = this;
	this.instance.setTransform(339.3,235.1,1,1,180,0,0,-49.1,0.2);

	this.timeline.addTween(cjs.Tween.get(this.instance).to({rotation:0,x:339.4,y:235},17).to({rotation:180,x:339.3,y:235.1},24).wait(6));

}).prototype = p = new cjs.MovieClip();


(lib.Scene_1_d2 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// d2
	this.instance = new lib.Tween1("synched",0);
	this.instance.parent = this;
	this.instance.setTransform(339.35,235,1,1,180,0,0,-96.7,0.7);

	this.timeline.addTween(cjs.Tween.get(this.instance).to({rotation:0,y:235.1},17).to({rotation:180,y:235},25).wait(5));

}).prototype = p = new cjs.MovieClip();


(lib.Scene_1_d1 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// d1
	this.instance = new lib.Tween2("synched",0);
	this.instance.parent = this;
	this.instance.setTransform(408.25,234.9);

	this.timeline.addTween(cjs.Tween.get(this.instance).to({regX:-68.9,regY:0.1,x:339.35,y:235},1).to({rotation:180,y:235.1},19).to({rotation:0,y:235},14).wait(13));

}).prototype = p = new cjs.MovieClip();


// stage content:
(lib.logo = function(mode,startPosition,loop) {
if (loop == null) { loop = false; }	this.initialize(mode,startPosition,loop,{});

	this.___GetDepth___ = function(obj) {
		var depth = obj.depth;
		var cameraObj = this.___camera___instance;
		if(cameraObj && cameraObj.depth && obj.isAttachedToCamera)
		{
			depth += depth + cameraObj.depth;
		}
		return depth;
		}
	this.___needSorting___ = function() {
		for (var i = 0; i < this.getNumChildren() - 1; i++)
		{
			var prevDepth = this.___GetDepth___(this.getChildAt(i));
			var nextDepth = this.___GetDepth___(this.getChildAt(i + 1));
			if (prevDepth < nextDepth)
				return true;
		}
		return false;
	}
	this.___sortFunction___ = function(obj1, obj2) {
		return (this.exportRoot.___GetDepth___(obj2) - this.exportRoot.___GetDepth___(obj1));
	}
	this.on('tick', function (event){
		var curTimeline = event.currentTarget;
		if (curTimeline.___needSorting___()){
			this.sortChildren(curTimeline.___sortFunction___);
		}
	});

	// timeline functions:
	this.frame_46 = function() {
		this.___loopingOver___ = true;
	}

	// actions tween:
	this.timeline.addTween(cjs.Tween.get(this).wait(46).call(this.frame_46).wait(1));

	// main_obj_
	this.main = new lib.Scene_1_main();
	this.main.name = "main";
	this.main.parent = this;
	this.main.setTransform(290.4,235.4,1,1,0,0,0,290.4,235.4);
	this.main.depth = 0;
	this.main.isAttachedToCamera = 0
	this.main.isAttachedToMask = 0
	this.main.layerDepth = 0
	this.main.layerIndex = 0
	this.main.maskLayerName = 0

	this.timeline.addTween(cjs.Tween.get(this.main).wait(47));

	// d1_obj_
	this.d1 = new lib.Scene_1_d1();
	this.d1.name = "d1";
	this.d1.parent = this;
	this.d1.setTransform(408.4,234.8,1,1,0,0,0,408.4,234.8);
	this.d1.depth = 0;
	this.d1.isAttachedToCamera = 0
	this.d1.isAttachedToMask = 0
	this.d1.layerDepth = 0
	this.d1.layerIndex = 1
	this.d1.maskLayerName = 0

	this.timeline.addTween(cjs.Tween.get(this.d1).wait(47));

	// d2_obj_
	this.d2 = new lib.Scene_1_d2();
	this.d2.name = "d2";
	this.d2.parent = this;
	this.d2.setTransform(242.7,235.8,1,1,0,0,0,242.7,235.8);
	this.d2.depth = 0;
	this.d2.isAttachedToCamera = 0
	this.d2.isAttachedToMask = 0
	this.d2.layerDepth = 0
	this.d2.layerIndex = 2
	this.d2.maskLayerName = 0

	this.timeline.addTween(cjs.Tween.get(this.d2).wait(47));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(386.9,280.8,225.89999999999998,227.8);
// library properties:
lib.properties = {
	id: '46DA4F4F7E89411CA5216CDF046C8633',
	width: 640,
	height: 480,
	fps: 24,
	color: "#FFFFFF",
	opacity: 1.00,
	manifest: [
		{src:"/static/img/logo_atlas_.png", id:"logo_atlas_"}
	],
	preloads: []
};



// bootstrap callback support:

(lib.Stage = function(canvas) {
	createjs.Stage.call(this, canvas);
}).prototype = p = new createjs.Stage();

p.setAutoPlay = function(autoPlay) {
	this.tickEnabled = autoPlay;
}
p.play = function() { this.tickEnabled = true; this.getChildAt(0).gotoAndPlay(this.getTimelinePosition()) }
p.stop = function(ms) { if(ms) this.seek(ms); this.tickEnabled = false; }
p.seek = function(ms) { this.tickEnabled = true; this.getChildAt(0).gotoAndStop(lib.properties.fps * ms / 1000); }
p.getDuration = function() { return this.getChildAt(0).totalFrames / lib.properties.fps * 1000; }

p.getTimelinePosition = function() { return this.getChildAt(0).currentFrame / lib.properties.fps * 1000; }

an.bootcompsLoaded = an.bootcompsLoaded || [];
if(!an.bootstrapListeners) {
	an.bootstrapListeners=[];
}

an.bootstrapCallback=function(fnCallback) {
	an.bootstrapListeners.push(fnCallback);
	if(an.bootcompsLoaded.length > 0) {
		for(var i=0; i<an.bootcompsLoaded.length; ++i) {
			fnCallback(an.bootcompsLoaded[i]);
		}
	}
};

an.compositions = an.compositions || {};
an.compositions['46DA4F4F7E89411CA5216CDF046C8633'] = {
	getStage: function() { return exportRoot.getStage(); },
	getLibrary: function() { return lib; },
	getSpriteSheet: function() { return ss; },
	getImages: function() { return img; }
};

an.compositionLoaded = function(id) {
	an.bootcompsLoaded.push(id);
	for(var j=0; j<an.bootstrapListeners.length; j++) {
		an.bootstrapListeners[j](id);
	}
}

an.getComposition = function(id) {
	return an.compositions[id];
}


// Layer depth API :

AdobeAn.Layer = new function() {
	this.getLayerZDepth = function(timeline, layerName)
	{
		if(layerName === "Camera")
		layerName = "___camera___instance";
		var script = "if(timeline." + layerName + ") timeline." + layerName + ".depth; else 0;";
		return eval(script);
	}
	this.setLayerZDepth = function(timeline, layerName, zDepth)
	{
		const MAX_zDepth = 10000;
		const MIN_zDepth = -5000;
		if(zDepth > MAX_zDepth)
			zDepth = MAX_zDepth;
		else if(zDepth < MIN_zDepth)
			zDepth = MIN_zDepth;
		if(layerName === "Camera")
		layerName = "___camera___instance";
		var script = "if(timeline." + layerName + ") timeline." + layerName + ".depth = " + zDepth + ";";
		eval(script);
	}
	this.removeLayer = function(timeline, layerName)
	{
		if(layerName === "Camera")
		layerName = "___camera___instance";
		var script = "if(timeline." + layerName + ") timeline.removeChild(timeline." + layerName + ");";
		eval(script);
	}
	this.addNewLayer = function(timeline, layerName, zDepth)
	{
		if(layerName === "Camera")
		layerName = "___camera___instance";
		zDepth = typeof zDepth !== 'undefined' ? zDepth : 0;
		var layer = new createjs.MovieClip();
		layer.name = layerName;
		layer.depth = zDepth;
		layer.layerIndex = 0;
		timeline.addChild(layer);
	}
}


})(createjs = createjs||{}, AdobeAn = AdobeAn||{});
var createjs, AdobeAn;
