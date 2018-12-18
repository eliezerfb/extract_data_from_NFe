unit Unit2;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls;

type
  TForm2 = class(TForm)
    Button1: TButton;
    procedure Button1Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Form2: TForm2;

implementation

{$R *.dfm}

uses ShellAPI;

procedure TForm2.Button1Click(Sender: TObject);
begin
  ShellExecute(0, nil, PChar('cmd.exe '), PChar('/c python D:\GitHubProjects\extract_data_from_NFe\is_ok.py'), nil, SW_HIDE);
end;

end.
