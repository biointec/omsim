#ifndef BASICPANEL_HPP
#define BASICPANEL_HPP

#include "wx.hpp"
#include <wx/stattext.h>

class BasicPanel : public wxPanel
{
        public:
                BasicPanel(wxWindow *parent, wxWindowID id)
                      : wxPanel(parent, id)
                {
                        wxBoxSizer *mainbox = new wxBoxSizer(wxVERTICAL);
                        
                        /*
                                xml box
                        */
                        wxBoxSizer *xmlbox = new wxBoxSizer(wxVERTICAL);
                        wxStaticText *xmlTitle = new wxStaticText(this, wxID_ANY, wxT("Configuration file"));
                        wxButton *xmlButton = new wxButton(this, -1, wxT("Open configuration file"));
                        xmlbox->Add(xmlTitle);
                        xmlbox->Add(xmlButton);
                        
                        /*
                                fasta box
                        */
                        wxBoxSizer *fastabox = new wxBoxSizer(wxVERTICAL);
                        wxStaticText *fastaTitle = new wxStaticText(this, wxID_ANY, wxT("Genome files"));
                        wxButton *ok = new wxButton(this, -1, wxT("Ok"));
                        fastabox->Add(fastaTitle);
                        fastabox->Add(ok);
                        
                        /*
                                enzyme box
                        */
                        wxBoxSizer *enzymebox = new wxBoxSizer(wxVERTICAL);
                        wxStaticText *enzymeTitle = new wxStaticText(this, wxID_ANY, wxT("Enzymes"));
                        wxButton *cancel = new wxButton(this, -1, wxT("Cancel"));
                        enzymebox->Add(enzymeTitle);
                        enzymebox->Add(cancel);
                        
                        /*
                                length box
                        */
                        wxBoxSizer *lengthbox = new wxBoxSizer(wxVERTICAL);
                        wxStaticText *lengthTitle = new wxStaticText(this, wxID_ANY, wxT("Size distribution"));
                        wxBoxSizer *sizedistbox = new wxBoxSizer(wxHORIZONTAL);
                        wxStaticText *meanText = new wxStaticText(this, wxID_ANY, wxT("Mean:"));
                        wxTextCtrl *mean = new wxTextCtrl(this, -1, wxT(""), wxPoint(-1, -1), wxSize(-1, -1));
                        wxStaticText *stdText = new wxStaticText(this, wxID_ANY, wxT("Standard deviation:"));
                        wxTextCtrl *std =  new wxTextCtrl(this, -1, wxT(""), wxPoint(-1, -1), wxSize(-1, -1));
                        sizedistbox->Add(meanText);
                        sizedistbox->Add(mean);
                        sizedistbox->Add(stdText);
                        sizedistbox->Add(std);
                        lengthbox->Add(lengthTitle);
                        lengthbox->Add(sizedistbox);
                        
                        
                        
                        mainbox->Add(xmlbox);
                        mainbox->Add(fastabox);
                        mainbox->Add(enzymebox);
                        mainbox->Add(lengthbox);
                        
                        SetSizer(mainbox);
                }
};

#endif
