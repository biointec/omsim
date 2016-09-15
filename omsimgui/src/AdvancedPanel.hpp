#ifndef ADVANCEDPANEL_HPP
#define ADVANCEDPANEL_HPP

#include "wx.hpp"

#include "configuration.hpp"

class TagPanel;

class AdvancedPanel : public wxPanel
{
        private:
                configuration &c;
                std::vector<TagPanel*> tags;
        public:
                AdvancedPanel(wxWindow *parent, wxWindowID id, configuration &c_);
                void update();
};

#endif
