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

  // ============================
  // Default Tasks
  // ============================

  /** HTML tasks **/

  gulp.task('html', function() {
    return gulp.src(['application/**/*.html'])
    .pipe(gulp.dest('dist/'));
  });

  /** CSS tasks **/

  gulp.task('app_css', function() {
    gulp.src('application/**/*.scss')
    .pipe(sass())
    .pipe(concat('app.css'))
    .on('error', sass.logError)
    .pipe(gulp.dest('.temp/css/'))
  });

  gulp.task('vendor_css', function() {
    return gulp.src(mainBowerFiles(), {
      base: './bower_components'
    })
    .pipe(filter('/**/*.css'))
    .pipe(concat('vendor.css'))
    .pipe(gulp.dest('.temp/css/'));
  });

  gulp.task('css', ['vendor_css', 'app_css'], function() {
    return gulp.src(['.temp/css/vendor.css', '.temp/css/app.css', 'bower_components/bootstrap/dist/css/bootstrap.css'])
    .pipe(concat('application.css'))
    .pipe(minifyCss({
      keepSpecialComments: 0
    }))
    .pipe(rename({
      extname: '.min.css'
    }))
    .pipe(gulp.dest('dist/css/'));
  });

  /** Font tasks **/

  gulp.task('vendor_fonts', function() {
    return gulp.src(mainBowerFiles(), {
      base: './bower_components'
    })
      .pipe(filter([
        '**/*.eot',
        '**/*.woff',
        '**/*.ttf',
        '**/*.svg'
      ]))
    .pipe(gulp.dest('dist/'));
  });

  gulp.task('app_fonts', function() {
    return gulp.src([
      'application/**/*.eot',
      'application/**/*.woff',
      'application/**/*.ttf',
      'application/**/*.svg'
    ])
    .pipe(gulp.dest('dist/fonts'));
  });

  gulp.task('fonts', ['vendor_fonts', 'app_fonts']);

  /** Image tasks **/

  gulp.task('images', function() {
    return gulp.src([
      'application/**/*.png',
      'application/**/*.jpg',
      'application/**/*.jpeg',
      'application/**/*.svg',
      'application/**/*.ico'
    ])
    .pipe(gulp.dest('dist/'));
  });

  /** JS tasks **/

  gulp.task('app_js', function() {
    return gulp.src(['application/**/*.module.js', 'application/**/*.component.js', 'application/**/*.js'])
    .pipe(concat('app.js'))
    .pipe(gulp.dest('.temp/js/'));
  });

  gulp.task('vendor_js', function() {
    return gulp.src(mainBowerFiles(), {
      base: './bower_components'
    })
    .pipe(filter('**/*.js'))
    .pipe(concat('vendor.js'))
    .pipe(gulp.dest('.temp/js/'));
  });

  gulp.task('js', ['vendor_js', 'app_js'], function() {
    return gulp.src(['.temp/js/vendor.js', '.temp/js/app.js'])
    .pipe(concat('application.js'))
    .pipe(uglify().on('error', gutil.log))
    .pipe(rename({
      extname: '.min.js'
    }))
    .pipe(gulp.dest('dist/js/'));
  });

  /** Watch tasks **/

  gulp.task('watch', function() {
    gulp.watch('application/**/*.html', ['html']);
    gulp.watch('application/**/*.js', ['app_js', 'js']);
    gulp.watch('application/**/*.scss', ['app_css', 'css']);
    connect.server({
      livereload: true,
      directoryListing: true,
      root: ['dist'],
      port: 3000
    });
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
    del('dist');
    del('.temp');
    del('coverage');
  });

  /** Terminal tasks **/
  gulp.task('scripts', ['app_js', 'vendor_js', 'js']);
  gulp.task('styles', ['app_css', 'vendor_css', 'css', 'fonts', 'images']);
  gulp.task('pack', ['html', 'scripts', 'styles']);
  gulp.task('default', ['html', 'scripts', 'styles', 'watch']);
    
})();