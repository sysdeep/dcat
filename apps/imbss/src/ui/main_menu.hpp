#ifndef MAIN_MENU
#define MAIN_MENU

namespace UI {
class MainMenu {
public:
  MainMenu();
  void draw();

private:
  bool _show_demo = false;
};
} // namespace UI

#endif // !DEBUG
