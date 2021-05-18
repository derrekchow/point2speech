var Tesseract = require('tesseract.js')
var fs = require('fs')
var say = require('say')
var watch = require('node-watch')

var image = "ocr.jpeg"

var wordData = []
var words = []

function Word(word, y, x0, x1, conf, index) {
	this.word = word
	this.y = y
	this.x0 = x0
	this.x1 = x1
	this.conf = Math.round(conf)
	this.index = index
	this.getInfo = function() {
		return "(\"" + this.word + "\", Y: " + this.y + ", X0: " + this.x0 + ", X1: " + this.x1 + ", conf: " + this.conf + ", index: " + this.index + ")"
	}
}

function speakAt(y, wordData, words) {
	for (j in wordData) {
		if (wordData[j].y == y) {
			var speakWords = words.splice(wordData[j].index)
			speakWords = speakWords.join(" ")
			console.log(speakWords)
			return speakWords
		}
	}
}

function tesseract() {
	console.log("starting tesseract...")
	Tesseract.recognize(image, {
		lang: 'eng'
	})
	.progress(function  (p) { 
		console.log(p)
	}).then(function(result){
		for (i in result.words) {
			var word = new Word(result.words[i].text, result.words[i].baseline.y0, result.words[i].baseline.x0, result.words[i].baseline.x1, result.words[i].confidence, i)
			wordData.push(word)
			words.push(result.words[i].text)
			console.log(word.getInfo())
		}
		text = result.text
		fs.writeFile('output.txt', text, function(err) {
			if(err) {
				console.log(err)
			}
		})
		console.log(wordData)
		console.log("Overall Confidence: " + result.confidence)
		console.log(text)
		//say.speak(speakAt(230, wordData, words))
	})
}

tesseract()




