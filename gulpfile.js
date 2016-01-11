'use strict'; 

// requirements 

var gulp = require('gulp'); 
var browserify = require('gulp-browserify');
var size = require('gulp-size'); 
var clean = require('gulp-clean'); 


// Tasks 
gulp.task('default', function() {
	console.log("Hello world !"); 
}); 

// Used to transform JSX into JS 
gulp.task('transform', function(){

	
	return gulp.src('./static/jsx/courses_react.js')
		.pipe(browserify({transform: ['reactify']}))
		.pipe(gulp.dest('./static/js'))
		.pipe(size()); 


}); 