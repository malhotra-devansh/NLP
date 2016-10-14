tp = [0.0, 0.0] # [ham, spam]
fp = [0.0, 0.0]
fn = [0.0, 0.0]

f1 = [0.0, 0.0]
precision = [0.0, 0.0]
recall = [0.0, 0.0]

with open('nboutput.txt','r') as f:
    for line in f:
        pred_class, path = line.split()
        true_class = path.split('/')[-1].split('.')[-2]

        if pred_class == 'ham' and true_class == 'ham':
            tp[0] += 1
        elif pred_class == 'ham' and true_class == 'spam':
            fp[0] += 1
            fn[1] += 1
        elif pred_class == 'spam' and true_class == 'ham':
            fn[0] += 1
            fp[1] += 1
        elif pred_class == 'spam' and true_class == 'spam':
            tp[1] += 1

for c in range(2):
    precision[c] = tp[c]/(tp[c] + fp[c])
    recall[c] = tp[c]/(tp[c] + fn[c])
    f1[c] = (2 * precision[c] * recall[c])/(precision[c] + recall[c])

print(precision)
print(recall)
print(f1)