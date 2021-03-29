const gulp = require('gulp');
const sass = require('gulp-sass');
const uglify = require('gulp-uglify-es').default;
const named = require('vinyl-named');
const webpack = require('webpack');
const webpackStream = require('webpack-stream');

function sassTask(done){
    return gulp.src([
        'src/scss/*.scss'
    ], {base:'src/'})
        .pipe(sass({
            outputStyle: 'compressed',
            errorLogToConsole: true,
        }))
        .on('error', console.log.bind(console))
        .pipe(gulp.dest('static/css/'))
        done()
}

function watchTask(done) {
    gulp.watch('src/scss/**/*.scss', sassTask); //Вызывает функцию sassTask, если scss файл изменился
    gulp.watch('src/js/**/*.js', jsTask); //Вызывает функцию js, если js файл изменился
    done()
}

function jsTask(done) {
    gulp.src([
        'src/js/*.js'
    ])
        .pipe(named()) //Сохраняем название точек
        .pipe(webpackStream({
            mode: "development",
            output: {
                filename: "[name].js",
                path: __dirname + '.',
            },
            module: {
                rules: [
                    {
                        exclude: /node_modules/, //runtime ищет не там где надо
                        use: {
                            loader: 'babel-loader',
                            options: {
                                presets: ['@babel/preset-env'],
                                plugins: [
                                    ['@babel/plugin-proposal-class-properties'],
                                    ['@babel/plugin-transform-runtime'],
                                ]
                            }
                        }
                    },
                ],
            },
        }), webpack)
        .pipe(uglify()) //Убираем переносы
        .on('error', function () {
            this.emit('end');
        })
        .pipe(gulp.dest('static/js/'))
    done()
}

gulp.task('default', gulp.parallel(sassTask, jsTask, watchTask))
