(function() {

  'use strict';

  var gulp = require('gulp');
  var gutil = require('gulp-util');
  var concat = require('gulp-concat');
  var sass = require('gulp-sass');
  var minifyCss = require('gulp-minify-css');
  var rename = require('gulp-rename');
  var uglify = require('gulp-uglify');
  var mainBowerFiles = require('main-bower-files');
  var karma = require('karma').server;
  var del = require('del');
  var filter = require('gulp-filter');
  var connect = require('gulp-connect');
  var runSequence = require('run-sequence');
  var order = require('gulp-order');

  /** Main **/

  gulp.task('default', ['pack'], function() {
    gulp.watch('application/**/*.*', ['pack']);
    connect.server({
      livereload: true,
      directoryListing: true,
      root: ['dist'],
      port: 8080
    });
  });

  gulp.task('pack', function(callback) {
    runSequence(
      'clean',
      'vendor_css',
      'vendor_js',
      'app_css',
      'app_js',
      'css',
      'js',
      'html',
      'static',
      'test',
      callback
    );
  });

  /** HTML **/

  gulp.task('html', function() {
    return gulp.src(['application/**/*.html'])
    .pipe(gulp.dest('dist/'));
  });

  /** Static **/

  gulp.task('static', function() {
    return gulp.src([
      'application/**/*.eot',
      'application/**/*.woff',
      'application/**/*.ttf',
      'application/**/*.svg',
      'application/**/*.png',
      'application/**/*.jpg',
      'application/**/*.jpeg',
      'application/**/*.svg',
      'bower_components/font-awesome/**/*.otf',
      'bower_components/font-awesome/**/*.eot',
      'bower_components/font-awesome/**/*.woff',
      'bower_components/font-awesome/**/*.woff2',
      'bower_components/font-awesome/**/*.ttf',
      'bower_components/font-awesome/**/*.svg'
    ])
    .pipe(rename({dirname: ''}))
    .pipe(gulp.dest('dist/fonts/'));
  });

  /** CSS **/

  gulp.task('app_css', function() {
    return gulp.src('application/**/*.scss')
    .pipe(sass())
    .pipe(concat('app.css'))
    .pipe(gulp.dest('.temp/css/'));
  });

  gulp.task('vendor_css', function() {
    return gulp.src('bower_components/**/*.css')
    .pipe(concat('vendor.css'))
    .pipe(gulp.dest('.temp/css/'));
  });

  gulp.task('css', function() {
    return gulp.src([
      '.temp/css/vendor.css',
      '.temp/css/app.css'
    ])
    .pipe(concat('application.css'))
    .pipe(minifyCss({
      keepSpecialComments: 0
    }))
    .pipe(rename({
      extname: '.min.css'
    }))
    .pipe(gulp.dest('dist/css/'));
  });

  /** JS **/

  gulp.task('app_js', function() {
    return gulp.src([
      'application/**/*.module.js',
      'application/**/*.component.js',
      'application/**/*.js'
    ])
    .pipe(concat('app.js'))
    .pipe(gulp.dest('.temp/js/'));
  });

  gulp.task('vendor_js', function() {
    return gulp.src(mainBowerFiles())
    .pipe(filter(['**/*.js']))
    .pipe(order([
      'jquery.js',
      'moment.js',
      'angular.js'
    ]))
    .pipe(concat('vendor.js'))
    .pipe(gulp.dest('.temp/js/'));
  });

  gulp.task('js', function() {
    return gulp.src([
      '.temp/js/vendor.js',
      '.temp/js/app.js'
    ])
    .pipe(concat('application.js'))
    .pipe(uglify().on('error', gutil.log))
    .pipe(rename({
      extname: '.min.js'
    }))
    .pipe(gulp.dest('dist/js/'));
  });

  /** Unit test tasks **/

  gulp.task('test', function(done) {
    karma.start({
      configFile: __dirname + '/test/test.conf.js',singleRun: true
    }, function() {
      done();
    });
  });

  /** Clean tasks **/

  gulp.task('clean', function() {
    return del(['.temp', 'dist']);
  });

})();
