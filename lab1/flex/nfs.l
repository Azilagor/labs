%{
#include <stdio.h>
#include <string.h>
#include <ctype.h>

char server[64];
int valid = 0;
FILE *yyin;

// Проверка, что путь корректен и не превышает 63 символа
int is_valid_path(const char* path) {
    if (strlen(path) > 63) return 0;

    const char* p = path;
    int slash_count = 0;
    while (*p) {
        if (*p == '/') {
            slash_count++;
            p++;
            continue;
        }

        if (!isalpha(*p)) return 0;

        // пройти имя до следующего слэша
        while (*p && *p != '/') {
            if (!isalpha(*p)) return 0;
            p++;
        }
    }
    return slash_count >= 1;
}
%}

%%
nfs://[a-zA-Z]+(/[a-zA-Z]+)* {
    valid = 0;
    char *full = strdup(yytext);
    char *path = full + 6;

    // Получаем имя сервера
    char *slash = strchr(path, '/');
    if (slash) {
        *slash = '\0';
        strncpy(server, path, sizeof(server));
        *slash = '/';
    } else {
        strncpy(server, path, sizeof(server));
    }

    if (is_valid_path(path)) {
        printf("OK: %s\n", yytext);
        printf("   -> сервер: %s\n", server);
        valid = 1;
    } else {
        printf("INVALID (bad path): %s\n", yytext);
    }

    free(full);
}

\n    { /* пропуск пустой строки */ }
.     { printf("INVALID (bad format): %s\n", yytext); }
%%

int yywrap() { return 1; }

int main() {
    FILE *fp = fopen("input.txt", "r");
    if (!fp) {
        perror("Ошибка открытия input.txt");
        return 1;
    }

    yyin = fp;
    yylex();
    fclose(fp);

    return 0;
}
