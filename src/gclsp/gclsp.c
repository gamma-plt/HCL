#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
 

typedef struct list {
    void *data;
    struct list *next;
} List;

void insert(List **p, void *data, unsigned int n)
{
    List *temp;
    int i;
    /* Error check is ignored */
    temp = malloc(sizeof(List));
    temp->data = malloc(n);
    for (i = 0; i < n; i++)
        *(char *)(temp->data + i) = *(char *)(data + i);
    temp->next = *p;
    *p = temp;
}

char* strstrip(char *s, char r) {
    size_t size = strlen(s);
    char* end;

    if (!size) return s;

    end = s + size - 1;

    while (end >= s && *end == r) end--;
    
    *(end + 1) = '\0';

    while (*s && *s == r) s++;

    return s;
}

char *replace(const char *s, char ch, const char *repl) {
    int count = 0;
    const char *t;
    for(t=s; *t; t++)
        count += (*t == ch);

    size_t rlen = strlen(repl);
    char *res = malloc(strlen(s) + (rlen-1)*count + 1);
    char *ptr = res;
    for(t=s; *t; t++) {
        if(*t == ch) {
            memcpy(ptr, repl, rlen);
            ptr += rlen;
        } else {
            *ptr++ = *t;
        }
    }
    *ptr = 0;
    return res;
}

struct node* read(void) {
    char* query = malloc(10 * sizeof(char*));
    char* copy = malloc(10 * sizeof(char*));
    char ch;
    int level = 0, balanced = 0, balance = 0;
    size_t length;

    printf(">> ");

    while(!balanced) {

        scanf("%c", &ch);
        length = strlen(query); 

        if(ch != '\n') {

            if(ch == '(') balance++;
            else if(ch == ')') balance--;

            if(balance < 0) {
                printf("Error while parsing query\n");
                break;
            }

            balanced = balance == 0;

            strcpy(copy, query);
            query = malloc(length + 2);            
            strcpy(query, copy);
            *(query + length) = ch;
            *(query + length + 1) = '\0';

            if(balanced) break;

        } else {

            if(strlen(strstrip(query, ' ')) == 0) return NULL;

            level++;

            strcpy(copy, query);
            query = malloc(length + 2);            
            strcpy(query, copy);
            *(query + length) = ' ';
            *(query + length + 1) = '\0';

            for(int i = 0; i < level; i++)
                printf("\t");
        }
    }

    query = strstrip(query, ' ');
    strcpy(copy, query);

    if(strlen(query) == 0)
        return NULL;

    query = replace(query, '(', " ( ");
    query = replace(query, ')', " ) ");

    int tokensnum = 0, i = 0;
    char *token = strtok(query, " ");
    while (token != NULL) {
        if(strlen(token) != 0)
            tokensnum++;
        token = strtok(NULL, " ");
    }

    char** tokens = malloc(tokensnum * sizeof(char**));
    token = strtok(copy, " ");
    while (token != NULL) {
        if(strlen(token) != 0) {
            *(tokens + i) = strstrip(token, '\t');
            i++;
        }
        token = strtok(NULL, " ");        
    }

    for(i = 0; *(tokens + i) != NULL; i++)
        printf("***%s %d\n", *(tokens + i), *(tokens + i) == NULL);

    return NULL;
} 



int main(int argc, char const *argv[]) {
    //read();

    char* str[] = {"Holla", "Hello", "Halo", "Chaito"};
    List* list;

    for(int i = 0; i < 4; i++) {
        char* current = *(str + i);
        insert(&list, current, strlen(current));
    }

    int i = 0;
    while(i < 4) {
        printf("%s\n", list->data);
        list = list->next;
        i++;
    }
    return 0;
}
 

 
/* 
int main()
{
    struct node *start = NULL;
    char* string = "Hola";
    push(&start, string, sizeof(string));
    string = "Bello";
    push(&start, string, sizeof(string));

    while (start != NULL) {
        printf("%s ", start->data);
        start = start->next;
    }

    printf("\n");
 
    return 0;
}
*/