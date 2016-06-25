#ifndef NOTEBOOK_HPP
#define NOTEBOOK_HPP

#include "wx.hpp"
#include <wx/notebook.h>
#include <wx/grid.h>

class Notebook : public wxFrame
{
        public:
                Notebook(const wxString& title);
                void OnQuit(wxCommandEvent& event);
};

#endif
