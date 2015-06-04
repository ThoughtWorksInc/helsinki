var gulp = require('gulp'),
    util = require('gulp-util'),
    sass = require('gulp-sass'),
    gulpif = require('gulp-if'),
    autoprefixer = require('gulp-autoprefixer'),
    minifyCSS = require('gulp-minify-css'),
    clean = require('gulp-clean');

var isDev  = true;
var isProd = false;
if(util.env.production === 'true') {
  isDev  = false;
  isProd = true;
}

var output_path = 'static';
var dev_path = {
  sass: ['sass/*.scss', '!sass/_*.scss']
};
var build_path = {
  css: output_path + '/css/'
};

gulp.task('sass', function () {
  return gulp.src(dev_path.sass)
      .pipe(sass({style: 'expanded', errLogToConsole: true}))
      .on('error', function(err) {
        console.log(err);
        this.emit('end');
      })
      .pipe(autoprefixer())
      .pipe(gulpif(isProd, minifyCSS({noAdvanced: true}))) // minify if Prod
      .pipe(gulp.dest(build_path.css));
});

gulp.task('clean-css', function () {
  return gulp.src([build_path.css], {read: false})
      .pipe(clean());
});

gulp.task('watch', function () {
  gulp.watch('sass/**/*.scss', ['sass']);
});

gulp.task('build', ['sass']);

gulp.task('default', ['sass','watch']);