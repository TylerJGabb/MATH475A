clear all
close all
clc
M = csvread('duck.csv');
x_vec = M(:,1);
f_vec = M(:,2);
p = polyfit(x_vec,f_vec,20)'
f_vec - polyval(p,x_vec)
test = linspace(0,14,100);
figure(1)
scatter(x_vec,f_vec);
hold on
plot(test,polyval(p,test))
ylim([0,3])
