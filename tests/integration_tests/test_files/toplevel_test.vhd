
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity toplevel_test is
  port (
  clock : in std_logic;

  LED : out std_logic_vector(15 downto 0);
  SW : in std_logic_vector(15 downto 0)
  ) ;
end toplevel_test ;

architecture arch of toplevel_test is

begin

  process(clock)
  begin
    if rising_edge(clock) then
      LED <= SW;
    end if;
  end process;

end architecture ; -- arch