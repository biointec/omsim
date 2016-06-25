#include "main.h"
#include "Notebook.h"

IMPLEMENT_APP(MyApp)

bool MyApp::OnInit()
{
        Notebook *notebook = new Notebook(wxT("Notebook"));
        notebook->Show(true);
        return true;
}
