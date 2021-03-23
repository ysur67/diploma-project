const gulp = require('gulp');
const sass = require('gulp-sass');
const uglify = require('gulp-uglify-es').default;
const named = require('vinyl-named');

function sassTask(done){
    return gulp.src([
        'src/scss/*.scss'
    ], {base:'src/'})
        .pipe(sass({
            outputStyle: 'compressed',
            errorLogToConsole: true,
        }))
        .on('error', console.log.bind(console))
        .pipe(gulp.dest('static/css/pages'))
        done()
}

function watchTask(done) {
    gulp.watch('src/scss/**/*.scss', sassTask); //Вызывает функцию sassTask, если scss файл изменился
    gulp.watch('src/js/**/*.js', jsTask); //Вызывает функцию js, если js файл изменился
    done()
}

function jsTask(done) {
    gulp.src([
        'src/js/pages/*.js'
    ])
        .pipe(named()) //Сохраняем название точек
        .pipe(uglify()) //Убираем переносы
        .on('error', function () {
            this.emit('end');
        })
        .pipe(gulp.dest('static/js/pages/'))
    done()
}

gulp.task('default', gulp.parallel(sassTask, jsTask, watchTask))
