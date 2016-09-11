var gulp = require('gulp'),
    loadPlugins = require('gulp-load-plugins')(),
    del = require('del'),
    tsConfig = require('./tsconfig.json');

gulp.task('build', function(){
  gulp.start('sass');
  gulp.start('html');
  gulp.start('scripts');
});

gulp.task('watch', ['build'], function(){
  gulp.watch('src/**/*.scss', function(){ gulp.start('sass'); });
  gulp.watch('src/**/*.html', function(){ gulp.start('html'); });
  gulp.watch('src/**/*.ts', function(){ gulp.start('scripts'); });
});

gulp.task('sass', function(){
  gulp.src('src/**/*.sass')
      .pipe(gulp.dest('www/app'));
});

gulp.task('html', function(){
  gulp.src('src/**/*.html')
      .pipe(gulp.dest('www/app'));
});

gulp.task('scripts', function(){
  gulp.src(['src/**/*.ts', 'typings/index.d.ts'])
      .pipe(loadPlugins.typescript(tsConfig.compilerOptions))
      .pipe(gulp.dest('www/app'));
});

gulp.task('clean', function(){
  return del('www/app');
});

gulp.task('serve', ['watch'], function(){
  gulp.src('.')
    .pipe(loadPlugins.webserver({
      host: '0.0.0.0',
      livereload: true,
      directoryListing: true
    }));
});
