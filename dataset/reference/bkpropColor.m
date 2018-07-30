
function [avgErr, Grad, latent, inputGrad] = backpropColor2( features,user, r, W,wInfo,extraLatent)

avgErr=0;
Grad=[];

weight1=reshape(W(wInfo.w1),wInfo.w1Size);
weight2=reshape(W(wInfo.w2),wInfo.w2Size);

features=features';
t =  [features  ones(1,size(features,1))'];
x1 = t*weight1;

%use the sigmoid activation function, and apply the second weights
y1 = [(1 ./ (1+ exp(-1.*x1)))];
x2 = [y1 ones(1,size(features,1))']*weight2;

%use the sigmoid activation function, and apply the third weights
%y2 =  [(1 ./ (1+ exp(-1.*x2)))];
%x3 = [y2 ones(1,size(features,1))']*weight3;

%use a linear output layer
y2=x2;

latent=y2;

if isempty(r)
    return
end


if exist('extraLatent','var')
    output=sum(user.*[extraLatent y2],2);
    dim=size(user,2)-size(extraLatent,2);
    backprobLatent=size(extraLatent,2)+1:size(user,2);
else
    output=sum(user.*y2,2);
    dim=size(user,2);
    backprobLatent=1:size(user,2);
end

err = 0.5*(output - r').^2;
avgErr = sum(sum(err)) /size(features,1) ;


%get the error going backward
dEdx2 = user(:,backprobLatent).*repmat(output - r',1,dim);
dEdw2 = [y1 ones(1,size(features,1))']' * dEdx2;


%compute the derivatives for the hidden units
%dEdy2 = weight3*dEdx3';
%dEdx2 = y2.*(1-y2) .* dEdy2(1:size(weight2,2),:)';
%dEdw2 = [y1 ones(1,size(features,1))']' * dEdx2; 

dEdy1 = weight2*dEdx2';
dEdx1 = y1.*(1-y1) .* dEdy1(1:size(weight2,1)-1,:)';
dEdw1 = t' *  dEdx1;

dEdt = weight1*dEdx1';

inputGrad=dEdt(1:size(weight1,1)-1,:)';

Grad=[dEdw1(:) ; dEdw2(:)];

