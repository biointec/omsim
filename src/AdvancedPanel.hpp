#ifndef ADVANCEDPANEL_HPP
#define ADVANCEDPANEL_HPP

#include "wx.hpp"

class AdvancedPanel : public wxPanel
{
        public:
                AdvancedPanel(wxWindow *parent, wxWindowID id)
                      : wxPanel(parent, id)
                {
                        wxBoxSizer *mainbox = new wxBoxSizer(wxVERTICAL);
                        
                        
                        wxBoxSizer *chipbox = new wxBoxSizer(wxVERTICAL);
                        
                        wxButton *ok = new wxButton(this, -1, wxT("Ok"));
                        chipbox->Add(ok);
                        
                        mainbox->Add(chipbox);
                        
                        
                        wxBoxSizer *fragilebox = new wxBoxSizer(wxVERTICAL);
                        
                        wxButton *cancel = new wxButton(this, -1, wxT("Cancel"));
                        fragilebox->Add(cancel);
                        
                        mainbox->Add(fragilebox);
                        
                        
                        SetSizerAndFit(mainbox);
                }
};

#endif
