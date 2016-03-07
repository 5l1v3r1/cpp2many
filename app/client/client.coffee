
sample = """
#include <iostream>
#include <vector>
using namespace std;

// euclid
int mcd (int a, int b) {
    while (a != b) {
        if (a > b) a = a - b;
        else b = b - a;
    }
    return a;
}

// main
int main () {
    cout << "Give me two numbers: ";
    int x, y;
    cin >> x >> y;
    int m = mcd(x, y);
    cout << "The mcd of " << x << " and " << y << " is " << m << endl;
}

"""


window.start_index = ->

    $(document).ready ->

        editor = ace.edit 'editor'

        editor.getSession().setMode 'ace/mode/c_cpp'
        #editor.setTheme 'ace/theme/monokai'
        editor.setShowPrintMargin false
        editor.renderer.setShowGutter true
        editor.getSession().setUseWrapMode false
        editor.setOptions
            minLines: 21
            maxLines: 21
            fontSize: '12pt'
            highlightActiveLine: false
        editor.setValue sample, -1
        editor.setValue sample, 1


        $editor = $('#editor')
        $editor.closest('form').submit ->
            console.log "subm"
            code = editor.getValue()
            $editor.prev('input[type=hidden]').val code



window.start_submission = ->

    $(document).ready ->
        hljs.initHighlightingOnLoad()


window.set_sample = ->

    editor = ace.edit 'editor'
    editor.setValue sample, -1
    editor.setValue sample, 1

