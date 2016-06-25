 #ifndef ENZYMEDIALOG_HPP
#define ENZYMEDIALOG_HPP

#include <wx/dialog.h>

struct enzyme {
        wxString id;
        wxString pattern;
        wxString label;
        wxString fn;
        wxString fp;
        
        enzyme(){}
        enzyme(wxString &id_, wxString &pattern_, wxString &label_, wxString &fn_, wxString &fp_)
              : id(id_), pattern(pattern_), label(label_), fn(fn_), fp(fp_)
        {
                
        }
};

class EnzymeDialog : public wxDialog
{
        private:
                
        public:
                EnzymeDialog(wxWindow *parent, wxWindowID id, const wxString &title, const wxPoint &pos=wxDefaultPosition, const wxSize &size=wxDefaultSize, long style=wxDEFAULT_DIALOG_STYLE, const wxString &name=wxDialogNameStr)
                      : wxDialog(parent, id, title, pos, size, style, name)
                {
                        
                }
                
};

#endif
