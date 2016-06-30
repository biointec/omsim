#include "Notebook.hpp"
#include "BasicPanel.hpp"
#include "AdvancedPanel.hpp"

Notebook::Notebook(wxWindow *parent, wxWindowID id, const wxString &title, const configuration &c_, const std::map<wxString, enzyme> &enzymes_, const wxPoint &pos, const wxSize &size, long style, const wxString &name)
      : wxDialog(parent, id, title, pos, size, style, name), c(c_), enzymes(enzymes_)
{
        wxNotebook *nb = new wxNotebook(this, -1, wxPoint(-1, -1), 
                wxSize(-1, -1), wxNB_TOP);
        
        BasicPanel *bpanel = new BasicPanel(nb, -1, c, enzymes);
        nb->AddPage(bpanel, wxT("Basic"));
        
        AdvancedPanel *apanel = new AdvancedPanel(nb, -1, c);
        nb->AddPage(apanel, wxT("Advanced"));
        
        Center();
}
